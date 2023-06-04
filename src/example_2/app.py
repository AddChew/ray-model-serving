from ray import serve
from pydantic import BaseModel
from access_key import api_key
from transformers import pipeline
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi import FastAPI, Depends, Security, HTTPException


app = FastAPI(
    title = 'Sentiment Analysis', 
    description = 'Documentation for Sentiment Analysis Model API'
)
api_key_header = APIKeyHeader(name = 'accessKey', auto_error = False)


class Payload(BaseModel):
    input_text: str


class Prediction(BaseModel):
    label: str
    score: float


class Message(BaseModel):
    detail: str


async def verify_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header != api_key:
        raise HTTPException(
            status_code = HTTP_401_UNAUTHORIZED,
            detail = 'Missing or invalid accessKey in request header.'
        )


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

    @app.post(
            path = '/model', 
            tags = ['Model Inference'], 
            summary = 'Model Inference on payload data',
            dependencies = [Depends(verify_api_key)],
            responses = {401: {'model': Message}}
    )
    async def predict(self, payload: Payload) -> Prediction:
        """
        Model Inference on payload data.
        """
        import os
        print(f'from process: {os.getpid()}')
        return self._classifier(payload.input_text)[0]
        

deployment = SentimentAnalysis.bind()