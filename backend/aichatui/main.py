from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from aichatui.models import BaseModel, Provider, Model
from aichatui.requests_responses import (
    ChatRequest, 
    ModelResponse,
    ModelRequest,
    ProviderResponse, 
    ProviderRequest, 
)
import aichatui.services.openai

engine = create_engine("sqlite:///sqlite.db", echo=True)
session = Session(engine)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    # Create db and tables
    BaseModel.metadata.create_all(engine)


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


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


@app.post("/chat-completion")
def chat_completion(chat_request: ChatRequest, db: Session = Depends(get_db)):
    model = db.get(Model, chat_request.model_id, options=[joinedload(Model.provider)])
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    # TODO make into actual web socket stream
    stream = aichatui.services.openai.query(model=model, query=chat_request.message)
    stream = list(stream)
    stream = "".join(stream)
    return {"message": stream}