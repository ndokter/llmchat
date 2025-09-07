from sqlalchemy.orm import Session

from aichatui.models import Chat, ChatMessage

from aichatui.tasks import run_chat_completion


def new_message(db: Session, chat_id, model_id, message):
    if chat_id:
        chat = db.get(Chat, chat_id)
    else:
        chat = Chat()
        db.add(chat)
        db.flush()

    user_message = ChatMessage(
        chat_id=chat.id,
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

    db.add(user_message)
    db.add(assistant_message)
    chat.messages.append(user_message)
    chat.messages.append(assistant_message)
    db.commit()

    task = run_chat_completion.delay(
        chat_id=chat_id,
        user_message_id=user_message.id,
        assistant_message_id=assistant_message.id
    )
    assistant_message.task_id = task.id
    db.commit()

    return assistant_message