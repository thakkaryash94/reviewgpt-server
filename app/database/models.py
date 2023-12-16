import enum
from sqlalchemy.sql import func
from sqlalchemy import JSON, TIMESTAMP, Boolean, Column, Enum, Integer, String
from app.database.database import Base


class OTHistoryEnum(enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    REJECTED = "REJECTED"
    FAILED = "FAILED"


class OTHistory(Base):
    __tablename__ = "ot_histories"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    ip_address = Column(String)
    ip_info = Column(JSON)
    status = Column(
        Enum(OTHistoryEnum),
        nullable=False,
        default=OTHistoryEnum.PENDING,
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
