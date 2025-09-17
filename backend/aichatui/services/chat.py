from sqlalchemy.orm import Session

from aichatui.models import Chat


def update(chat: Chat, title: str, db: Session):
    chat.title = title

    db.commit()

    return chat


def delete(chat: Chat, db: Session):
    db.delete(chat)
    db.commit()