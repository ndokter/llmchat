import json
from celery.contrib.abortable import AbortableTask
from sqlalchemy.orm import joinedload

from aichatui.database import db_session
from aichatui.models import ChatMessage
from aichatui.config import settings
from aichatui.celery_utils import celery_app
from aichatui.services.openai import Roles
from aichatui.services.event_stream import PubSubProducer, EventType
import aichatui.services.openai
import aichatui.services.chat
import aichatui.selectors.chat
import aichatui.selectors.model


@celery_app.task(bind=True, base=AbortableTask)
def run_chat_completion(self, assistant_message_id):
    with db_session() as db:
        assistant_message = (
            db.query(ChatMessage)
            .options(joinedload(ChatMessage.parent), joinedload(ChatMessage.chat))
            .filter(ChatMessage.id == assistant_message_id)
            .first()
        )
        chat = assistant_message.chat

        events = aichatui.services.openai.query(
            model=assistant_message.model,
            messages=[
                {"role": message.role, "content": message.message}
                for message in chat.messages
            ],
        )

        with PubSubProducer(settings.REDIS_URL, channel="chat-events") as pub:
            for event in events:
                if self.is_aborted():
                    break

                if content := event.choices[0].delta.content:
                    assistant_message.message += content
                    pub.send(
                        {
                            "type": EventType.CHAT_COMPLETION,
                            "body": {
                                "chat_id": chat.id,
                                "message_id": assistant_message.id,
                                "status": assistant_message.status,
                                "content": assistant_message.message,
                            },
                        }
                    )

        if self.is_aborted():
            assistant_message.status = ChatMessage.STATUS_CANCELLED
        else:
            assistant_message.status = ChatMessage.STATUS_COMPLETED

        pub.send(
            {
                "type": EventType.CHAT_COMPLETION,
                "body": {
                    "chat_id": chat.id,
                    "message_id": assistant_message.id,
                    "status": assistant_message.status,
                    "content": assistant_message.message,
                },
            }
        )

        db.commit()

        run_title_generation(chat_id=chat.id)


def run_title_generation(chat_id):
    with db_session() as db:
        chat = aichatui.selectors.chat.get_or_create(chat_id=chat_id, db=db)
        title_model = aichatui.selectors.model.get_title_generation_model(db=db)
        title_prompt = aichatui.services.chat.generate_title_prompt(chat=chat, db=db)

        events = aichatui.services.openai.query(
            model=title_model,
            messages=[{"role": Roles.ROLE_USER, "content": title_prompt}]
        )

        title_json = ""
        for event in events:
            if content := event.choices[0].delta.content:
                title_json += content


        try:
            title = json.loads(title_json)['title']
        except json.JSONDecodeError:
            return

        chat.title = title
        db.commit()

        with PubSubProducer(settings.REDIS_URL, channel="chat-events") as pub:
            pub.send({
                "type": EventType.CHAT_TITLE,
                "body": {"title": chat.title}
            })