import datetime
from typing import Optional
from pydantic import BaseModel as PydanticBaseModel, ConfigDict


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True)


class ChatRequest(BaseModel):
    chat_id: int | None
    message: str
    model_id: int


class ChatResponse(BaseModel):
    id: int
    title: str
    
    # messages: Mapped[list["ChatMessage"]] = relationship(
    #     "ChatMessage", 
    #     back_populates="chat",
    #     cascade="all, delete-orphan"
    # )


class ProviderResponse(BaseModel):
    id: int
    url: str
    api_key: str

    class Config:
        from_attributes = True


class ProviderRequest(BaseModel):
    url: str
    api_key: str


class ModelResponse(BaseModel):
    id: int
    name: str
    alias: str
    system_prompt: Optional[str]
    provider_id: int

    class Config:
        from_attributes = True


class ModelRequest(BaseModel):
    name: str
    alias: str
    system_prompt: Optional[str] = None
    provider_id: int


class ChatMessageResponse(BaseModel):
    id: int
    role: str
    message: str
    status: str
    token_count: int|None
    created_at: datetime.datetime

    chat_id: int
    model_id: int
    task_id: str