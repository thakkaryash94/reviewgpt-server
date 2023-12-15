from sqlalchemy import update
from sqlalchemy.orm import Session
from app.database import models, schemas


def create_othistory(db: Session, item: schemas.OTHistoryCreate):
    db_item = models.OTHistory(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_othistory(db: Session, item: schemas.OTHistory):
    update_statement = (
        update(models.OTHistory)
        .where(models.OTHistory.id == item.id)
        .values(is_done=item.is_done)
    )
    db_item = db.execute(update_statement)
    db.commit()
    return db_item
