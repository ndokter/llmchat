from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from aichatui.models import Chat


def get_or_create(chat_id: int, db: Session):
    if chat_id:
        chat = db.get(Chat, chat_id)
    else:
        chat = Chat()
        db.add(chat)
        db.flush()

    return chat


def get_with_message(chat_id: int, db: Session) -> Chat:
    return db.query(Chat) \
        .options(joinedload(Chat.messages)) \
        .filter(Chat.id == chat_id) \
        .first()


def get_list(db: Session):
    return db.scalars(
        select(Chat).order_by(Chat.id.desc())
    ).all()

