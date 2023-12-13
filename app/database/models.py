from sqlalchemy.sql import func
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String
from .database import Base


class History(Base):
    __tablename__ = "histories"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    ip_address = Column(String)
    url = Column(String)
    is_done = Column(Boolean, nullable=False, default=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now()
    )
