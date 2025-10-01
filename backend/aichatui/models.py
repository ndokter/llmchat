from dataclasses import Field
from typing import List
from typing import Optional
import datetime

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from aichatui.database import Base


class BaseModel(Base):
    __abstract__ = True


class Provider(BaseModel):
    __tablename__ = "provider"
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str]
    api_key: Mapped[str]

    models: Mapped[List["Model"]] = relationship(
        back_populates="provider"
    )


class Model(BaseModel):
    __tablename__ = "model"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    alias: Mapped[str]
    system_prompt: Mapped[Optional[str]]
    deleted_at: Mapped[Optional[datetime.datetime]]

    provider_id: Mapped[Optional[int]] = mapped_column(ForeignKey("provider.id", ondelete="SET NULL"))
    provider: Mapped["Provider"] = relationship(back_populates="models")

    messages: Mapped[list["ChatMessage"]] = relationship(
        back_populates="model"
    )


class Chat(BaseModel):
    __tablename__ = "chat"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[Optional[str]]
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        index=True
    )
    
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

    # Assistant role specific fields
    prompt_tokens: Mapped[Optional[int]] = mapped_column()
    completion_tokens: Mapped[Optional[int]] = mapped_column()
    total_tokens: Mapped[Optional[int]] = mapped_column()

    model_id: Mapped[Optional[int]] = mapped_column(ForeignKey("model.id"))
    model: Mapped[Optional["Model"]] = relationship()
    task_id:  Mapped[Optional[str]] = mapped_column(String(36))

    # Other relations
    chat_id: Mapped[int] = mapped_column(ForeignKey("chat.id"))
    chat: Mapped["Chat"] = relationship(back_populates="messages")
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("chat_message.id"))
    parent: Mapped[Optional["ChatMessage"]] = relationship(
        remote_side=[id], 
        back_populates="children"
    )
    children: Mapped[List["ChatMessage"]] = relationship(
        back_populates="parent",
        cascade="all, delete-orphan"
    )