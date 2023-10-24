"""
Модуль валидации типов
"""

from datetime import datetime
from pydantic import BaseModel
from typing import List


class FeedRequest(BaseModel):
    """
    Класс FeedRequest для валидации типов при подаче
    сервису входных признаков запроса ленты.
    """
    user_id: int
    request_time: datetime
    posts_limit: int = 5


class PostGet(BaseModel):
    """
    Класс PostGet для валидации типов постов при
    выдаче рекомендаций
    """
    post_id: int
    text: str
    topic: str


class FeedResponse(BaseModel):
    """
    Класс FeedResponse для валидации типов отклика при
    выдаче ленты постов
    """
    feed: List[PostGet] = []
