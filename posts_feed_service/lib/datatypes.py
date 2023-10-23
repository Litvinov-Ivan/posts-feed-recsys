from datetime import datetime
from pydantic import BaseModel
from typing import List


class FeedRequest(BaseModel):
    user_id: int
    request_time: datetime
    posts_limit: int = 5


class PostGet(BaseModel):
    post_id: int
    text: str
    topic: str


class FeedResponse(BaseModel):
    recommendations: List[PostGet]
