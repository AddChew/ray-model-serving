import logging
from ray import serve
from datetime import datetime
from fastapi import FastAPI


app = FastAPI()


class DummyModelPipeline:

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return "I am a dummy model pipeline"


@serve.deployment
class DummyShapPipeline:

    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.logger = logging.getLogger("ray.serve")

    def write_to_file(self): # TODO: integrate with tenacity retry, add logging for attempt and create flaky function
        self.logger.info(self.name)
        time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        filepath = f'./{time}.txt'
        with open(filepath, "w") as f:
            f.write(time + " " + self.name)
        return "Write to file successfully"
    

@serve.deployment(name = 'sentiment-analysis', route_prefix = '/model', num_replicas = 1)
@serve.ingress(app)
class SentimentAnalysis:

    def __init__(self, explainer):
        self._classifier = DummyModelPipeline()
        self._explainer = explainer

    @app.post("/predict")
    async def predict(self, input_text: str) -> str:
        self._explainer.write_to_file.remote()
        return self._classifier(input_text)


explainer = DummyShapPipeline.bind("hi")
model = SentimentAnalysis.bind(explainer)