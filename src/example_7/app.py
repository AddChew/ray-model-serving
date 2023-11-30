from ray import serve
from fastapi import FastAPI
from factory import DummyModelPipeline, actor


app = FastAPI()


@serve.deployment(name = 'sentiment-analysis', route_prefix = '/model', num_replicas = 1)
@serve.ingress(app)
class SentimentAnalysis:

    def __init__(self):
        self._classifier = DummyModelPipeline()

    @app.post("/predict")
    async def predict(self, input_text: str) -> str:
        actor.write_to_file.remote()
        return self._classifier(input_text)

deployment = SentimentAnalysis.bind()