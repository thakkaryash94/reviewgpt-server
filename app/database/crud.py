from sqlalchemy import update
from sqlalchemy.orm import Session
from app.database import models, schemas


def count_othistory_by_ip(db: Session, ip_address: str):
    count = (
        db.query(models.OTHistory)
        .filter(models.OTHistory.ip_address == ip_address)
        .count()
    )
    return count


def create_othistory(db: Session, item: schemas.OTHistoryCreate):
    db_item = models.OTHistory(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_othistory(db: Session, item: schemas.OTHistoryUpdate):
    update_statement = (
        update(models.OTHistory)
        .where(models.OTHistory.id == item.id)
        .values(status=item.status)
    )
    db_item = db.execute(update_statement)
    db.commit()
    return db_item
