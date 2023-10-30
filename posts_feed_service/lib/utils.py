"""
Модуль для преобразования переданных в сервис
запросов для последующей передачи
и получения ленты постов.
"""

import pandas as pd
from typing import Dict


def get_group(user_id: int) -> int:
    """
    Функция получения группы пользователя для
    проведения A\B теста
    """
    # найти хэш-функцию из ДЗ
    return 1


def request_transform(
        request: dict,
        exp_group: int,
        tables: Dict[str, pd.DataFrame]
) -> pd.DataFrame:
    """
    Функция преобразования признаков запроса.
    """
    # добавить загрузку эмбеддингов
    request_df = tables["posts"].copy()
    request_df = request_df.merge(
        tables["posts_tfidf"], on='post_id'
    ).drop(['text'], axis=1)
    request_df['month'] = request["request_time"].month
    request_df['hour'] = request["request_time"].hour
    request_df['day'] = request["request_time"].day
    request_df['weekday'] = request["request_time"].weekday()
    user_df = tables["users"][
        tables["users"]['user_id'] == request["user_id"]
    ]
    request_df = request_df.merge(user_df, how='cross')
    return request_df.drop(['post_id', 'user_id'], axis=1)
