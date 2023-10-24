"""
Модуль сервиса персональных рекоммендаций новостей.

С помощью ручки /feed можно послать POST запрос с JSONом и
получить ленту новостей.
"""


from fastapi import FastAPI
from lib.datatypes import FeedRequest, FeedResponse
from lib.model import Model


model = Model()
app = FastAPI()


@app.post("/feed")
def feed(request: FeedRequest) -> FeedResponse:
    """
    Ручка выдачи ленты новостей

    Ручке передаётся JSON с id пользователя и временем запроса,
    возвращается список рекоменндованных данному пользователю постов.
    """
    recommendations = model.get_feed(request.dict())
    return recommendations
