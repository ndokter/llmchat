# aichatui/tasks.py
from celery import shared_task
from fastapi import Depends
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from aichatui.models import ChatMessage
import aichatui.services.openai

engine = create_engine("sqlite:///sqlite.db", echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_celery_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


@shared_task
def run_chat_completion(user_message_id, assistant_message_id):

    db_generator = get_celery_db()
    db: Session = next(db_generator) 

    user_message = db.get(ChatMessage, user_message_id)
    assistant_message = db.get(ChatMessage, assistant_message_id)

    stream = aichatui.services.openai.query(
        model=assistant_message.model, 
        query=user_message.message
    )
    stream = list(stream)
    print(stream)
    stream = "".join(stream)

    assistant_message.message = stream
    db.commit()