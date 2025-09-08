from celery import shared_task

from sqlalchemy.orm import joinedload

from aichatui.database import db_session
from aichatui.models import ChatMessage
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

        for event in events:
            if content:= event.choices[0].delta.content:
                # REDIS channel
                message += content
        
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