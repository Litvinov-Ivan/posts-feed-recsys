"""
Модуль для преобразования переданных в сервис
запросов для последующей передачи
и получения ленты постов.
"""

import pandas as pd
from typing import Dict


def request_transform(request: dict, tables: Dict[pd.DataFrame]) -> pd.DataFrame:
    """
    Функция преобразования признаков запроса.
    """
    request_df = tables["posts"].copy()
    request_df = request_df.merge(
        tables["posts_tfidf"], on='post_id'
    ).drop(['text'], axis=1)
    request_df['month'] = request["request_time"].month.astype(int)
    request_df['hour'] = request["request_time"].hour.astype(int)
    request_df['day'] = request["request_time"].day.astype(int)
    request_df['weekday'] = request["request_time"].weekday().astype(int)
    user_df = tables["users"][
        tables["users"]['user_id'] == request["user_id"]
    ]
    request_df = request_df.merge(user_df, how='cross')
    return request_df.drop(['post_id', 'user_id'], axis=1)
