import numpy as np
from ray import serve
from typing import Dict
from fastapi import FastAPI
from transformers import pipeline
from ray.util.metrics import Histogram


app = FastAPI()


DEFAULT_MODEL = 'distilbert-base-uncased-finetuned-sst-2-english'


@serve.deployment(name = 'sentiment-analysis', route_prefix = '/model', num_replicas = 1)
@serve.ingress(app)
class SentimentAnalysis:

    def __init__(self):
        # Code in __init__ will only run once in each replica on startup
        # Normally, will load the model here
        self.model = DEFAULT_MODEL
        self._classifier = pipeline(task = 'sentiment-analysis', model = self.model)
        self.histogram = Histogram(
            "model_scores",
            description = "Model scores",
            boundaries = np.linspace(0.1, 1, 10),
        )

    @app.post("/predict")
    async def predict(self, input_text: str) -> Dict:
        sentiment = self._classifier(input_text)[0]
        self.histogram.observe(sentiment["score"])
        if input_text:
            return {
                'sentiment': sentiment,
                'model': self.model,
            }
        return {'message': 'Please provide input_text for inference.'}

deployment = SentimentAnalysis.bind()