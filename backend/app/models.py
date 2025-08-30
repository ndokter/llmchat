from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class BaseModel(DeclarativeBase):
    pass


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