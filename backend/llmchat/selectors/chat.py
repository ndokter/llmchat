from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from llmchat.models import Chat


def get_with_message(chat_id: int, db: Session) -> Chat:
    return (
        db.query(Chat)
        .options(joinedload(Chat.messages))
        .filter(Chat.id == chat_id)
        .first()
    )


def get_list(db: Session):
    return db.scalars(select(Chat).order_by(Chat.id.desc())).all()
