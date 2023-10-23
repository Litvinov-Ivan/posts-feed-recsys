from pathlib import Path
import yaml
from catboost import CatBoostClassifier
import pandas as pd
from datatypes import FeedRequest, FeedResponse


CONFIG_DIR = Path(__file__).parent
CONFIG_PATH = CONFIG_DIR / "config.yaml"
with open(CONFIG_PATH, "r", encoding="utf-8") as config_file:
    CONFIG = yaml.load(config_file, Loader=yaml.FullLoader)

class Model:
    def __init__(self):
        self.model = CatBoostClassifier()
        self.model.load_model(CONFIG["classifier_model"])
        self.posts = pd.read_csv(CONFIG["post_df"])
        self.users = pd.read_csv(CONFIG["user_df"])
        self.tf_idf_df = pd.read_csv(CONFIG["tf_idf_df"])

    def get_feed(self, request: dict) -> FeedResponse:
        pass
