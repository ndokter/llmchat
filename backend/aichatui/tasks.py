from celery import shared_task

from aichatui.database import db_session
from aichatui.models import ChatMessage
import aichatui.services.openai


@shared_task
def run_chat_completion(user_message_id, assistant_message_id):

    with db_session() as db:
        user_message = db.get(ChatMessage, user_message_id)
        assistant_message = db.get(ChatMessage, assistant_message_id)

        stream = aichatui.services.openai.query(
            model=assistant_message.model, 
            query=user_message.message
        )
        stream = list(stream)
        print(stream)
        stream = "".join(stream)

        # user_message = 

        assistant_message.message = stream
        assistant_message.status = ChatMessage.STATUS_COMPLETED
        db.commit()