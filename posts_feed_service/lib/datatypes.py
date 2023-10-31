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
    user_id: int = 200
    request_time: datetime = datetime(2022, 1, 31)
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
    exp_group: str = ""
    feed: List[PostGet] = []
