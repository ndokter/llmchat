from celery import shared_task

from sqlalchemy.orm import joinedload

from aichatui.database import db_session
from aichatui.models import Chat, ChatMessage
import aichatui.services.openai


@shared_task
def run_chat_completion(chat_id, user_message_id, assistant_message_id):

    with db_session() as db:
        chat = db.query(Chat).options(joinedload(Chat.messages)).get(chat_id)
        user_message = db.get(ChatMessage, user_message_id)
        assistant_message = db.get(ChatMessage, assistant_message_id)

        events = aichatui.services.openai.query(
            model=assistant_message.model, 
            messages=[
                {'role': message.role, 'content': message.message}
                for message in chat.messages
            ]
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

        user_message.token_count = event.usage.prompt_tokens
        assistant_message.message = message
        assistant_message.token_count = event.usage.completion_tokens
        #assistant_message.token_count_total = event.usage.total_tokens
        
        assistant_message.status = ChatMessage.STATUS_COMPLETED

        db.commit()