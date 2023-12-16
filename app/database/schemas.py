from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, JsonValue, RootModel

from app.database.models import OTHistoryEnum


class ResponseBase(BaseModel):
    code: int
    message: str
    success: bool


class ReviewResponseData(BaseModel):
    result: bool
    positive: str
    negative: str


class ReviewResponse(ResponseBase):
    data: ReviewResponseData | None = None


class OTHistoryBase(BaseModel):
    ip_address: str | None = None
    ip_info: JsonValue | None = None
    url: str
    status: OTHistoryEnum


class OTHistory(OTHistoryBase):
    id: int

    class Config:
        from_attributes = True


class OTHistoryCreate(OTHistoryBase):
    pass


class OTHistoryUpdate(OTHistoryBase):
    pass


class Review(BaseModel):
    title: str
    content: str
    author: str
    is_verified: bool
    rating: int
    rating_limit: int
    created_at: Optional[datetime] = None


class ReviewList(RootModel):
    root: List[Review]
