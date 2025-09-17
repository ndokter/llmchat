import datetime
from typing import List, Optional
from pydantic import BaseModel as PydanticBaseModel, ConfigDict


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True)


class ProviderResponse(BaseModel):
    id: int
    url: str
    api_key: str


class ProviderRequest(BaseModel):
    url: str
    api_key: str


class ModelRequest(BaseModel):
    name: str
    alias: str
    system_prompt: Optional[str] = None
    provider_id: int


class ModelResponse(BaseModel):
    id: int
    name: str
    alias: str
    system_prompt: Optional[str]
    provider_id: int


class ChatMessageResponse(BaseModel):
    id: int
    role: str
    message: str
    status: str
    prompt_tokens: int|None
    completion_tokens: int|None
    total_tokens: int|None
    created_at: datetime.datetime

    chat_id: int
    model_id: Optional[int] = None
    task_id: Optional[str] = None
    parent_id: Optional[int] = None


class ChatRequest(BaseModel):
    chat_id: int | None
    model_id: int
    parent_id: int | None
    message: str


class ChatUpdateRequest(BaseModel):
    title: Optional[str] = None


class ChatResponse(BaseModel):
    id: int
    title: Optional[str] = None
    
    messages: List[ChatMessageResponse] = []


class ChatListResponse(BaseModel):
    id: int
    title: Optional[str] = None