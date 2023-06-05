import logging
from ray import serve
from pydantic import BaseModel

from access_key import api_key
from transformers import pipeline
from fastapi.security.api_key import APIKeyHeader
from fastapi import FastAPI, Depends, Security, HTTPException, status


app = FastAPI(
    title = 'Sentiment Analysis', 
    description = 'Documentation for Sentiment Analysis Model API'
)
api_key_header = APIKeyHeader(name = 'accessKey', auto_error = False)


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.INFO)
streamHandler.setFormatter(formatter)

fileHandler = logging.FileHandler('/home/addison/Documents/Github/Repositories/ray-model-serving/test.log')
fileHandler.setLevel(logging.INFO)
fileHandler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(streamHandler)
logger.addHandler(fileHandler)


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
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Missing or invalid accessKey in request header.'
        )


@serve.deployment(
    name = 'sentiment-analysis', 
    autoscaling_config = {
        "min_replicas": 2,
        "initial_replicas": 2,
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
        try:
            logger.info('Loading model pipeline...')
            self._pipeline = pipeline('sentiment-analysis')
            logger.info('Loaded model pipeline successfully.')
        except Exception as e:
            logger.error(str(e))
            self._pipeline = None

    @app.post(
            path = '/model', 
            tags = ['Model Inference'], 
            summary = 'Model Inference on payload data',
            dependencies = [Depends(verify_api_key)],
            responses = {401: {'model': Message}, 501: {'model': Message}}
    )
    async def predict(self, payload: Payload) -> Prediction:
        """
        Model Inference on payload data.
        """
        import os
        print(f'from process: {os.getpid()}')
        if self._pipeline is None:
            raise HTTPException(
                status_code = status.HTTP_501_NOT_IMPLEMENTED,
                detail = 'Unable to load model pipeline.'
            )
        return self._pipeline(payload.input_text)[0]
        

deployment = SentimentAnalysis.bind()