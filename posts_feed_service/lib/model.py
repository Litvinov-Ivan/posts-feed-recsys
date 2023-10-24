"""
Модуль класса Model.

Предназначен для загрузки всех необходимых
датасетов и модели при старте сервиса вместе с
инициализацией объекта класса и для получения
ленты новостей при запросах в сервисе.
"""

import yaml
import pandas as pd
import numpy as np
from pathlib import Path
from catboost import CatBoostClassifier
from lib.datatypes import FeedResponse, PostGet
from lib.utils import request_transform


CONFIG_DIR = Path(__file__).parent
CONFIG_PATH = CONFIG_DIR / "config.yaml"
with open(CONFIG_PATH, "r", encoding="utf-8") as config_file:
    CONFIG = yaml.load(config_file, Loader=yaml.FullLoader)


class Model:
    """
    Класс Model для получения ленты новостей
    """
    def __init__(self):
        """
        Конструктор класса Model

        Загружает всё необходимое для обработки
        признаков и получения ленты.
        """
        self.model = CatBoostClassifier()
        self.model.load_model(CONFIG["classifier_model"])
        self.tables = {
            "posts": pd.read_csv(CONFIG["post_df"]),
            "users": pd.read_csv(CONFIG["user_df"]),
            "posts_tfidf": pd.read_csv(CONFIG["tfidf_df"]),
        }

    async def get_feed(self, request: dict) -> FeedResponse:
        """
        Метод получения предсказания цены автомобиля.

        Производит обработку признаков запроса и
        получает рекомендованные новости.
        """
        posts_limit = request["posts_limit"]
        request = request_transform(request, self.tables)
        col_order = self.model.feature_names_
        feed_prediction = self.model.predict_proba(request[col_order])[:, 1]
        indices = np.argpartition(
            feed_prediction,
            -posts_limit
        )[-posts_limit:]
        result_feed = self.tables["posts"].iloc[indices].reset_index()
        recs = FeedResponse()
        for i, post in result_feed.iterrows():
            recs.feed.append(
                PostGet(
                    post_id=post["post_id"],
                    text=post["text"],
                    topic=post["topic"]
                )
            )
        return recs
