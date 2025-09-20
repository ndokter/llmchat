from celery.contrib.abortable import AbortableTask
from sqlalchemy.orm import joinedload

from aichatui.database import db_session
from aichatui.models import ChatMessage
from aichatui.services.event_stream import PubSubProducer
from aichatui.config import settings
from aichatui.celery_utils import celery_app
import aichatui.services.openai


@celery_app.task(bind=True, base=AbortableTask)
def run_chat_completion(self, assistant_message_id):

    with db_session() as db:
        assistant_message = db.query(ChatMessage) \
            .options(joinedload(ChatMessage.parent),
                     joinedload(ChatMessage.chat)) \
            .filter(ChatMessage.id == assistant_message_id) \
            .first()
        chat = assistant_message.chat

        events = aichatui.services.openai.query(
            model=assistant_message.model, 
            messages=[{'role': message.role, 'content': message.message}
                      for message in chat.messages]
        )

        with PubSubProducer(settings.REDIS_URL, channel="chat-events") as pub:
            for event in events:
                if self.is_aborted():
                    break

                if content := event.choices[0].delta.content:
                    assistant_message.message += content
                    pub.send({
                        "type": "chat:completion",
                        "chat_id": chat.id,
                        "message_id": assistant_message.id,
                        "status": assistant_message.status,
                        "content": assistant_message.message
                    })

        if self.is_aborted():
            assistant_message.status = ChatMessage.STATUS_CANCELLED
            pub.send({
                "type": "chat:completion",
                "chat_id": chat.id,
                "message_id": assistant_message.id,
                "status": assistant_message.status,
                "content": assistant_message.message
            })
        else:
            assistant_message.status = ChatMessage.STATUS_COMPLETED
            pub.send({
                "type": "chat:completion",
                "chat_id": chat.id,
                "message_id": assistant_message.id,
                "status": assistant_message.status,
                "content": assistant_message.message
            })

        db.commit()