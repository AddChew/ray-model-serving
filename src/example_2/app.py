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

# TODO: api key
@serve.deployment(
    name = 'sentiment-analysis', 
    autoscaling_config = {
        "min_replicas": 1,
        "initial_replicas": 1,
        "max_replicas": 5,
        "target_num_ongoing_requests_per_replica": 10,
        "downscale_delay_s": 600,
        "upscale_delay_s": 30,
    },
)
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
        import os
        print(f'from process: {os.getpid()}')
        return self._classifier(payload.input_text)[0]
        

deployment = SentimentAnalysis.bind()