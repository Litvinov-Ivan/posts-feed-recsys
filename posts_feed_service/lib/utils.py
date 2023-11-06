"""
Модуль для преобразования переданных в сервис
запросов для последующей передачи
и получения ленты постов.
"""

import pandas as pd
import numpy as np
from typing import Dict
from hashlib import md5


def get_group(user_id: int, 
              groups_num: int = 2,
              salt: str = "my_salt") -> str:
    """
    Функция получения группы пользователя для
    проведения A\B теста
    """
    group = int(
        md5((str(user_id) + salt).encode()).hexdigest(), 
        16
    ) % groups_num
    if group:
        return "test"
    return "control"


def request_transform(
        request: dict,
        exp_group: str,
        tables: Dict[str, pd.DataFrame]
) -> pd.DataFrame:
    """
    Функция преобразования признаков запроса.
    """
    request_df = tables["posts"].copy()
    request_df = request_df.merge(
        tables["posts_tfidf"], on="post_id"
    ).drop(["text"], axis=1)
    request_df["month"] = request["request_time"].month
    request_df["hour"] = request["request_time"].hour
    request_df["day"] = request["request_time"].day
    request_df["weekday"] = request["request_time"].weekday()

    if exp_group == "test":
        text_w2v_cols = [f"text_w2v_{i}" for i in range(1, 11)]
        cols = ['post_id'] + text_w2v_cols
        request_df = request_df.merge(
            tables["embs_post_df"][cols], on="post_id"
        )

    if request["user_id"] not in tables["users"]["user_id"].unique():
        user_df = pd.DataFrame().from_dict(
            {
                "user_id": np.array(request["user_id"]),
                "gender": tables["users"].gender.mode().values,
                "age": tables["users"].age.mode().values,
                "country": tables["users"].country.mode().values,
                "city": tables["users"].city.mode().values,
                "exp_group": tables["users"].exp_group.mode().values,
                "os": tables["users"].os.mode().values,
                "source": tables["users"].source.mode().values,
            }
        )
    else:
        user_df = tables["users"][
            tables["users"]["user_id"] == request["user_id"]
        ]

    request_df = request_df.merge(user_df, how="cross")

    return request_df.drop(["post_id", "user_id"], axis=1)
