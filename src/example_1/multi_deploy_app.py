from ray import serve
from typing import Dict
from transformers import pipeline
from starlette.requests import Request


class FactoryDeployment:

    DEFAULT_MODEL = 'distilbert-base-uncased-finetuned-sst-2-english'

    def __init__(self):
        self.model = self.DEFAULT_MODEL
        self.classifier = pipeline(task = "sentiment-analysis", model = self.model)

    def reconfigure(self, config: Dict):
        self.model = config.get("model", self.DEFAULT_MODEL)
        self.classifier = pipeline(task = "sentiment-analysis", model = self.model)

    async def __call__(self, input_text: str) -> Dict:
        if input_text:
            return {
                'sentiment': self.classifier(input_text)[0],
                'model': self.model,
            }
        return {'message': 'Please provide input_text for inference.'}


@serve.deployment(name = "deployment-1", num_replicas = 1, user_config = {"model": "distilbert-base-uncased-finetuned-sst-2-english"})
class Deployment1(FactoryDeployment):
    pass


@serve.deployment(name = "deployment-2", num_replicas = 1, user_config = {"model": "ahmedrachid/FinancialBERT-Sentiment-Analysis"})
class Deployment2(FactoryDeployment):
    DEFAULT_MODEL = "ahmedrachid/FinancialBERT-Sentiment-Analysis"


@serve.deployment(name = "driver", route_prefix = "/model", num_replicas = 1)
class Driver:

    def __init__(self, deployment1, deployment2):
        self.deployment1 = deployment1
        self.deployment2 = deployment2

    async def __call__(self, request: Request) -> Dict:
        payload = await request.json()
        model = payload.get("model")
        input_text = payload.get("input_text")

        classifier = self.deployment1
        if model == "ahmedrachid/FinancialBERT-Sentiment-Analysis":
            classifier = self.deployment2

        ref = await classifier.remote(input_text)
        return await ref
    
deployment1 = Deployment1.bind()
deployment2 = Deployment2.bind()
driver = Driver.bind(deployment1, deployment2)