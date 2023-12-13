from sqlalchemy.orm import Session
from . import models, schemas


def create_history(db: Session, history: schemas.HistoryCreate):
    db_item = models.History(**history.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
