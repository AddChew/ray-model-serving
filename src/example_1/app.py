from ray import serve
from typing import Dict
from transformers import pipeline
from fastapi import FastAPI
from starlette.requests import Request


app = FastAPI(
    root_path = "/serve"
)

DEFAULT_MODEL = 'distilbert-base-uncased-finetuned-sst-2-english'


@serve.deployment(name = 'sentiment-analysis', route_prefix = '/model1', num_replicas = 1, user_config = {"model": DEFAULT_MODEL})
@serve.ingress(app)
class SentimentAnalysis:

    def __init__(self):
        # Code in __init__ will only run once in each replica on startup
        # Normally, will load the model here
        self.model = DEFAULT_MODEL
        self._classifier = pipeline(task = 'sentiment-analysis', model = self.model)

    def reconfigure(self, config: dict):
        self.model = config.get("model", DEFAULT_MODEL)
        self._classifier = pipeline(task = 'sentiment-analysis', model = self.model)

    @app.post("/predict")
    async def predict(self, input_text: str) -> Dict:
        # payload = await request.json()
        # input_text = payload.get('input_text')
        if input_text:
            return {
                'sentiment': self._classifier(input_text)[0],
                'model': self.model,
            }
        return {'message': 'Please provide input_text for inference.'}
    
@serve.deployment(name = 'sentiment-analysis2', route_prefix = '/model2', num_replicas = 1, user_config = {"model": DEFAULT_MODEL})
@serve.ingress(app)
class SentimentAnalysis2:

    def __init__(self):
        # Code in __init__ will only run once in each replica on startup
        # Normally, will load the model here
        self.model = DEFAULT_MODEL
        self._classifier = pipeline(task = 'sentiment-analysis', model = self.model)

    def reconfigure(self, config: dict):
        self.model = config.get("model", DEFAULT_MODEL)
        self._classifier = pipeline(task = 'sentiment-analysis', model = self.model)

    @app.post("/predict")
    async def predict(self, input_text: str) -> Dict:
        # payload = await request.json()
        # input_text = payload.get('input_text')
        if input_text:
            return {
                'sentiment': self._classifier(input_text)[0],
                'model': self.model,
            }
        return {'message': 'Please provide input_text for inference.'}

deployment1 = SentimentAnalysis.bind()
deployment2 = SentimentAnalysis2.bind()