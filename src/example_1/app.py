from ray import serve
from typing import Dict
from transformers import pipeline
from starlette.requests import Request


@serve.deployment(name = 'sentiment-analysis', route_prefix = '/model', num_replicas = 1)
class SentimentAnalysis:

    def __init__(self):
        # Code in __init__ will only run once in each replica on startup
        # Normally, will load the model here
        self._classifier = pipeline('sentiment-analysis')

    async def __call__(self, request: Request) -> Dict:
        payload = await request.json()
        input_text = payload.get('input_text')
        if input_text:
            return self._classifier(input_text)[0]
        return {'message': 'Please provide input_text for inference.'}


deployment = SentimentAnalysis.bind()