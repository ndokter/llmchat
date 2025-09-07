from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from aichatui.database import get_db, engine
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
import aichatui.services.chat

@asynccontextmanager
async def lifespan(app: FastAPI):
    BaseModel.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)
celery_app = create_celery()


@app.get("/providers", response_model=list[ProviderResponse])
def provider_list(db: Session = Depends(get_db)):
    providers = db.scalars(select(Provider)).all()

    return providers


@app.post("/providers", response_model=ProviderResponse)
def provider_create(provider_request: ProviderRequest, db: Session = Depends(get_db)):
    provider = Provider(
        url=provider_request.url, 
        api_key=provider_request.api_key
    )

    db.add(provider)
    db.commit()
    db.refresh(provider)
    
    return provider


@app.put("/providers/{provider_id}", response_model=ProviderResponse)
def provider_update(provider_id: int, provider_request: ProviderRequest, db: Session = Depends(get_db)):
    provider = db.get(Provider, provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    provider.url = provider_request.url
    provider.api_key = provider_request.api_key
    
    db.commit()
    db.refresh(provider)

    return provider


@app.delete("/providers/{provider_id}")
def provider_delete(provider_id: int, db: Session = Depends(get_db)):
    provider = db.get(Provider, provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    db.delete(provider)
    db.commit()
    
    return Response(status_code=204)


@app.get("/models", response_model=list[ModelResponse])
def model_list(db: Session = Depends(get_db)):
    models = db.scalars(select(Model)).all()

    return models


@app.post("/models", response_model=ModelResponse)
def model_create(model_request: ModelRequest, db: Session = Depends(get_db)):
    model = Model(
        name=model_request.name, 
        alias=model_request.alias, 
        system_prompt=model_request.system_prompt,
        provider_id=model_request.provider_id
    )

    db.add(model)
    db.commit()
    db.refresh(model)
    
    return model


@app.put("/models/{model_id}", response_model=ModelResponse)
def model_update(model_id: int, model_request: ModelRequest, db: Session = Depends(get_db)):
    model = db.get(Model, model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Provider not found")
    model.name = model_request.name
    model.alias = model_request.alias
    model.system_prompt = model_request.system_prompt
    model.provider_alias = model_request.provider_id

    db.commit()
    db.refresh(model)

    return model


@app.delete("/models/{model_id}")
def model_delete(model_id: int, db: Session = Depends(get_db)):
    model = db.get(Model, model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    db.delete(model)
    db.commit()
    
    return Response(status_code=204)



# TODO POST chats/
# TODO GET  chats/
# TODO GET  chats/<id>
# TODO POST chats/<id>/messages
# TODO POST chats/<id>/stream


@app.get("/chats")
def chats_list(db: Session = Depends(get_db)):
    return []


@app.post("/chats", response_model=ChatMessageResponse)
def chat_new_message(chat_request: ChatRequest, db: Session = Depends(get_db)):
    assistant_message = aichatui.services.chat.new_message(
        db=db,
        chat_id=chat_request.chat_id, 
        model_id=chat_request.model_id, 
        message=chat_request.message,
    )

    return assistant_message


@app.get("/chats/{chat_id}")
def chat_details(request: Request, chat_id: int, db: Session = Depends(get_db)):
    return {}


@app.get("/chats/{chat_id}/messages")
def chat_messages(request: Request, chat_id: int, db: Session = Depends(get_db)):
    return {}


@app.get("/chats/{chat_id}/stream")
async def chat_stream(request: Request, chat_id: int, db: Session = Depends(get_db)):
    return ''