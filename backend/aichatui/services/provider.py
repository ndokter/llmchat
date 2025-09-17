from sqlalchemy.orm import Session

from aichatui.models import Provider


def update(provider: Provider, url: str, api_key: str, db: Session):
    provider.url = url
    provider.api_key = api_key
    
    db.commit()

    return provider


def delete(provider: Provider, db: Session):
    import aichatui.services.models

    # Soft delete models first
    for model in provider.models:
        aichatui.services.models.delete(model=model, db=db)

    db.delete(provider)
    db.commit()