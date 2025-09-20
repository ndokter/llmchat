from typing import Optional

from celery.contrib.abortable import AbortableAsyncResult
from sqlalchemy.orm import Session

from aichatui.models import Chat, ChatMessage
from aichatui.tasks import run_chat_completion
from aichatui.models import ChatMessage
from aichatui.celery_utils import celery_app


def create(
    chat: Chat, 
    parent_id: Optional[int], 
    model_id: int, 
    message: ChatMessage, 
    db: Session
):
    user_message = ChatMessage(
        chat_id=chat.id,
        parent_id=parent_id,
        role=ChatMessage.ROLE_USER,
        message=message,
        status=ChatMessage.STATUS_COMPLETED
    )
    assistant_message = ChatMessage(
        chat_id=chat.id,
        role=ChatMessage.ROLE_ASSISTANT,
        message="",
        status=ChatMessage.STATUS_GENERATING,
        model_id=model_id,
    )
    assistant_message.parent = user_message

    db.add(user_message)
    db.add(assistant_message)
    chat.messages.append(user_message)
    chat.messages.append(assistant_message)
    db.commit()

    task = run_chat_completion.delay(assistant_message_id=assistant_message.id)
    assistant_message.task_id = task.id

    db.commit()

    return assistant_message


def cancel(chat_message: ChatMessage, db: Session):
    result = AbortableAsyncResult(chat_message.task_id, app=celery_app)
    result.abort()