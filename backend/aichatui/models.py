from typing import List
from typing import Optional
import datetime

from aichatui.database import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class BaseModel(Base):
    __abstract__ = True


class Provider(BaseModel):
    __tablename__ = "provider"
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str]
    api_key: Mapped[str]

    models: Mapped[List["Model"]] = relationship(back_populates="provider", cascade="all, delete-orphan")


class Model(BaseModel):
    __tablename__ = "model"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    alias: Mapped[str]
    system_prompt: Mapped[Optional[str]]

    provider_id: Mapped[int] = mapped_column(ForeignKey("provider.id"))
    provider: Mapped["Provider"] = relationship(back_populates="models")


class Chat(BaseModel):
    __tablename__ = "chat"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[Optional[str]]
    
    messages: Mapped[list["ChatMessage"]] = relationship(
        "ChatMessage", 
        back_populates="chat",
        cascade="all, delete-orphan"
    )


class ChatMessage(BaseModel):
    __tablename__ = "chat_message"

    ROLE_USER = "user"
    ROLE_ASSISTANT = "assistant"

    STATUS_GENERATING = "generating"
    STATUS_COMPLETED = "completed"
    STATUS_FAILED = "failed"
    STATUS_CANCELLED = "cancelled"

    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str]  # user/assistant
    message: Mapped[str]
    status: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)

    chat_id: Mapped[int] = mapped_column(ForeignKey("chat.id"))
    chat: Mapped["Chat"] = relationship(back_populates="messages")

    token_count: Mapped[Optional[int]] = mapped_column()

    # Assistant role specific fields
    model_id: Mapped[Optional[int]] = mapped_column(ForeignKey("model.id"))
    model: Mapped[Optional["Model"]] = relationship()
    task_id:  Mapped[Optional[str]] = mapped_column(String(36))