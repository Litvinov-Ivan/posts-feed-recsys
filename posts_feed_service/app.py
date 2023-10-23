from fastapi import FastAPI
from lib.datatypes import FeedRequest, FeedResponse
from lib.model import Model


model = Model()
app = FastAPI()


@app.post("/feed")
def feed(request: FeedRequest) -> FeedResponse:
    recommendations = model.get_feed(request.dict())
    return recommendations
