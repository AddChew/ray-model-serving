from ray import serve
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline


app = FastAPI(
    title = 'Sentiment Analysis', 
    description = 'Documentation for Sentiment Analysis Model API'
)


class Payload(BaseModel):
    input_text: str


class Prediction(BaseModel):
    label: str
    score: float


@serve.deployment(name = 'sentiment-analysis', num_replicas = 1)
@serve.ingress(app)
class SentimentAnalysis:

    def __init__(self):
        # Code in __init__ will only run once in each replica on startup
        # Normally, will load the model here
        self._classifier = pipeline('sentiment-analysis')

    @app.post('/model', tags = ['Model Inference'], description = 'Model Inference on payload data.')
    def predict(self, payload: Payload) -> Prediction:
        """
        Model Inference on payload data.
        """
        return self._classifier(payload.input_text)[0]
        

deployment = SentimentAnalysis.bind()