from contextlib import asynccontextmanager
import redis.asyncio as aioredis
import asyncio
import json

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse

from llmchat.config import settings
from llmchat.database import get_db, engine
from llmchat.models import BaseModel, Provider, Model, ChatMessage
from llmchat.requests_responses import (
    ChatRequest,
    ChatUpdateRequest,
    ChatResponse,
    ChatListResponse,
    ChatMessageResponse,
    ModelResponse,
    ModelRequest,
    ProviderResponse,
    ProviderRequest,
)
from llmchat.celery_utils import celery_app
import llmchat.services.chat
import llmchat.services.chat_message
import llmchat.services.models
import llmchat.services.provider
import llmchat.selectors.chat
import llmchat.selectors.model


@asynccontextmanager
async def lifespan(app: FastAPI):
    BaseModel.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

celery_app.autodiscover_tasks(["llmchat"])


@app.post("/providers", response_model=ProviderResponse)
def provider_create(provider_request: ProviderRequest, db: Session = Depends(get_db)):
    provider = Provider(url=provider_request.url, api_key=provider_request.api_key)

    db.add(provider)
    db.commit()
    db.refresh(provider)

    return provider


@app.get("/providers", response_model=list[ProviderResponse])
def provider_list(db: Session = Depends(get_db)):
    providers = db.scalars(select(Provider)).all()

    return providers


@app.get("/providers/{provider_id}", response_model=ProviderResponse)
def provider_details(provider_id: int, db: Session = Depends(get_db)):
    provider = db.get(Provider, provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    return provider


@app.put("/providers/{provider_id}", response_model=ProviderResponse)
def provider_update(
    provider_id: int, provider_request: ProviderRequest, db: Session = Depends(get_db)
):
    provider = db.get(Provider, provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    provider = llmchat.services.provider.update(
        provider=provider,
        url=provider_request.url,
        api_key=provider_request.api_key,
        db=db,
    )

    return provider


@app.delete("/providers/{provider_id}")
def provider_delete(provider_id: int, db: Session = Depends(get_db)):
    provider = db.get(Provider, provider_id)  # TODO joinedload/selector
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    llmchat.services.provider.delete(provider=provider, db=db)

    return Response(status_code=204)


@app.get("/models", response_model=list[ModelResponse])
def model_list(db: Session = Depends(get_db)):
    select_models = select(Model).where(Model.deleted_at == None)
    models = db.scalars(select_models).all()

    return models


@app.post("/models", response_model=ModelResponse)
def model_create(model_request: ModelRequest, db: Session = Depends(get_db)):
    model = Model(
        name=model_request.name,
        alias=model_request.alias,
        system_prompt=model_request.system_prompt,
        provider_id=model_request.provider_id,
    )

    db.add(model)
    db.commit()
    db.refresh(model)

    return model


@app.put("/models/{model_id}", response_model=ModelResponse)
def model_update(
    model_id: int, model_request: ModelRequest, db: Session = Depends(get_db)
):
    model = db.get(Model, model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Provider not found")

    model = llmchat.services.models.update(
        model=model,
        name=model_request.name,
        alias=model_request.alias,
        system_prompt=model_request.system_prompt,
        db=db,
    )

    return model


@app.delete("/models/{model_id}")
def model_delete(model_id: int, db: Session = Depends(get_db)):
    model = db.get(Model, model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    llmchat.services.models.delete(model=model, db=db)

    return Response(status_code=204)


@app.post("/chat-message", response_model=ChatResponse)
async def chat_new_message(chat_request: ChatRequest, db: Session = Depends(get_db)):
    model = llmchat.selectors.model.active_by_id(model_id=chat_request.model_id, db=db)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    if chat_request.parent_id:
        parent_message = db.get(ChatMessage, chat_request.parent_id)
        if not parent_message:
            raise HTTPException(status_code=404, detail="Parent message not found")
        parent_message_id = parent_message.id
    else:
        parent_message_id = None

    chat = llmchat.services.chat.get_or_create(chat_id=chat_request.chat_id, db=db)
    llmchat.services.chat_message.create(
        chat=chat,
        parent_id=parent_message_id,
        model_id=model.id,
        message=chat_request.message,
        db=db,
    )

    return chat


@app.get("/chats", response_model=list[ChatListResponse])
async def chats_list(db: Session = Depends(get_db)):
    return llmchat.selectors.chat.get_list(db=db)


@app.get("/chats/{chat_id}", response_model=ChatResponse)
async def chat_details(request: Request, chat_id: int, db: Session = Depends(get_db)):
    chat = llmchat.selectors.chat.get_with_message(chat_id=chat_id, db=db)

    if not chat:
        return Response(status_code=404)

    return chat


@app.put("/chats/{chat_id}", response_model=ChatResponse)
async def chat_update(
    chat_update_request: ChatUpdateRequest, chat_id: int, db: Session = Depends(get_db)
):
    chat = llmchat.selectors.chat.get_with_message(chat_id=chat_id, db=db)
    chat = llmchat.services.chat.update(
        chat=chat, title=chat_update_request.title, db=db
    )

    return chat


@app.delete("/chats/{chat_id}", response_model=ChatResponse)
async def chat_delete(request: Request, chat_id: int, db: Session = Depends(get_db)):
    chat = llmchat.selectors.chat.get_with_message(chat_id=chat_id, db=db)
    llmchat.services.chat.delete(chat=chat, db=db)

    return Response(status_code=204)


@app.get("/messages/{message_id}", response_model=ChatMessageResponse)
async def chat_message_details(
    request: Request, message_id: int, db: Session = Depends(get_db)
):
    chat_message = db.get(ChatMessage, message_id)
    return chat_message


@app.delete("/messages/{message_id}")
async def chat_message_delete(message_id: int, db: Session = Depends(get_db)):
    chat_message = db.get(ChatMessage, message_id)
    if not chat_message:
        raise HTTPException(status_code=404, detail="Chat message not found")

    db.delete(chat_message)
    db.commit()

    return Response(status_code=204)


@app.post("/messages/{message_id}/cancel")
async def chat_message_cancel(message_id: int, db: Session = Depends(get_db)):
    chat_message = db.get(ChatMessage, message_id)
    if not chat_message:
        raise HTTPException(status_code=404, detail="Chat message not found")

    llmchat.services.chat_message.cancel(chat_message=chat_message, db=db)

    return Response(status_code=204)


@app.get("/event-stream")
async def event_stream(request: Request):
    async def event_generator(redis_url: str, channel: str):
        redis = aioredis.from_url(redis_url)
        pubsub = redis.pubsub()
        try:
            await pubsub.subscribe(channel)

            while True:
                msg = await pubsub.get_message(timeout=10)
                if msg is None:
                    yield b": keep-alive\n\n"
                elif msg["type"] == "message":
                    payload = json.dumps(json.loads(msg["data"]))
                    yield f"data: {payload}\n\n".encode("utf-8")
        except asyncio.CancelledError:
            raise
        finally:
            await pubsub.close()
            await redis.close()

    return StreamingResponse(
        event_generator(settings.REDIS_URL, "chat-events"),
        media_type="text/event-stream; charset=utf-8",
    )
