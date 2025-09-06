from celery import Celery
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from aichatui.models import BaseModel, Provider, Model, Chat, ChatMessage
from aichatui.requests_responses import (
    ChatRequest, 
    ChatMessageResponse,
    ModelResponse,
    ModelRequest,
    ProviderResponse, 
    ProviderRequest, 
)
from aichatui.tasks import run_chat_completion
from aichatui.celery_utils import create_celery
import aichatui.services.openai

def new_message(chat=None, ):
    if not chat:
        chat = Chat()
        db.add(chat)
        db.flush()

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