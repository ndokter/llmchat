from typing import Optional
from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    model_id: int


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

