from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, RootModel


class ResponseBase(BaseModel):
    code: int
    message: str
    success: bool


class ReviewResponseData(BaseModel):
    result: bool
    positive: str
    negative: str


class ReviewResponse(ResponseBase):
    data: ReviewResponseData


class HistoryCreate(BaseModel):
    email: str
    ip_address: str | None = None
    url: str

    class Config:
        from_attributes = True


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
