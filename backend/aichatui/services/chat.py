from sqlalchemy.orm import Session

from aichatui.models import Chat, ChatMessage

from aichatui.tasks import run_chat_completion


# TODO improve args
def new_message(chat_request, db: Session):
    if chat_request.chat_id:
        chat = db.get(Chat, chat_request.chat_id)
    else:
        chat = Chat()
        db.add(chat)
        db.flush()

    user_message = ChatMessage(
        chat_id=chat.id,
        role=ChatMessage.ROLE_USER,
        message=chat_request.message,
        status=ChatMessage.STATUS_COMPLETED
    )
    db.add(user_message)

    assistant_message = ChatMessage(
        chat_id=chat.id,
        role=ChatMessage.ROLE_ASSISTANT,
        message="",
        status=ChatMessage.STATUS_GENERATING,
        model_id=chat_request.model_id,
    )
    db.add(assistant_message)
    chat.messages.append(user_message)
    db.commit()

    task = run_chat_completion.delay(
        user_message_id=user_message.id,
        assistant_message_id=assistant_message.id
    )
    assistant_message.task_id = task.id
    db.commit()

    return assistant_message