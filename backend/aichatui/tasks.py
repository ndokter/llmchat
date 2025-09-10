import time
from celery import shared_task
from sqlalchemy.orm import joinedload
import redis

from aichatui.database import db_session
from aichatui.models import ChatMessage
from aichatui.services.redis import ChatMessageStreamProducer
import aichatui.services.openai
from aichatui.config import settings


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

        with ChatMessageStreamProducer(
            redis_url=settings.REDIS_URL,
            channel_name=f'message-{assistant_message_id}'
        ) as chat_channel:
            # Stream events from inference provider
            for event in events:
                if content:= event.choices[0].delta.content:
                    message += content

                    # Put them on the a redis channel for live streaming
                    chat_channel.add_message(content)

        if not event:
            assistant_message.status = ChatMessage.STATUS_FAILED
            db.commit()
            return

        assistant_message.message = message
        assistant_message.prompt_tokens = event.usage.completion_tokens
        assistant_message.completion_tokens = event.usage.completion_tokens
        assistant_message.total_tokens = event.usage.total_tokens
        
        assistant_message.status = ChatMessage.STATUS_COMPLETED

        db.commit()