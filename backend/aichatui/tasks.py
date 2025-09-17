from celery import shared_task
from sqlalchemy.orm import joinedload

from aichatui.database import db_session
from aichatui.models import ChatMessage
from aichatui.services.event_stream import EventStreamProducer
from aichatui.config import settings
import aichatui.services.openai


@shared_task
def run_chat_completion(assistant_message_id):

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

        event = None
        message = ""

        with EventStreamProducer(
            redis_url=settings.REDIS_URL,
            channel_name='chat-events'
        ) as stream:

            for event in events:
                if content:= event.choices[0].delta.content:
                    message += content

                    stream.add_message(
                        {
                            "type": "chat:completion",
                            "chat_id": chat.id,
                            "message_id": assistant_message.id,
                            "status": assistant_message.status,
                            "content": content
                        }
                    )

        if not event:
            assistant_message.status = ChatMessage.STATUS_FAILED
            db.commit()
            return

        assistant_message.message = message
        assistant_message.prompt_tokens = event.usage.completion_tokens
        assistant_message.completion_tokens = event.usage.completion_tokens
        assistant_message.total_tokens = event.usage.total_tokens
        assistant_message.status = ChatMessage.STATUS_COMPLETED

        stream.add_message(
            {
                "type": "chat:completion",
                "chat_id": chat.id,
                "message_id": assistant_message.id,
                "status": assistant_message.status,
                "content": ""
            }
        )

        db.commit()