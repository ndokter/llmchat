from sqlalchemy import select
from sqlalchemy.orm import Session

from aichatui.models import Model


def active_by_id(model_id: int, db: Session):
    return db.scalar(select(Model)
        .where(Model.id == model_id)
        .where(Model.deleted_at.is_(None))
    )


def get_title_generation_model(db: Session):
    return db.query(Model).one()
