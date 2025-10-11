from sqlalchemy.orm import Session

from llmchat.models import Provider


def update(provider: Provider, url: str, api_key: str, db: Session):
    provider.url = url
    provider.api_key = api_key
    
    db.commit()

    return provider


def delete(provider: Provider, db: Session):
    import llmchat.services.models

    # Soft delete models first
    for model in provider.models:
        llmchat.services.models.delete(model=model, db=db)

    db.delete(provider)
    db.commit()