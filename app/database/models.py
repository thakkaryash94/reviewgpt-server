from sqlalchemy.sql import func
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String
from app.database.database import Base


class OTHistory(Base):
    __tablename__ = "ot_histories"
    id = Column(Integer, primary_key=True)
    ip_address = Column(String)
    url = Column(String)
    is_done = Column(Boolean, nullable=False, default=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())
