import datetime
from sqlalchemy.orm import Session

from llmchat.models import Model


def update(model: Model, name: str, alias: str, system_prompt:str, db: Session):
    model.name = name
    model.alias = alias
    model.system_prompt = system_prompt
    
    db.commit()

    return model


def delete(model: Model, db: Session):
    model.deleted_at = datetime.datetime.now()
    db.commit()