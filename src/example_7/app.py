import logging
import numpy as np
from ray import serve
from datetime import datetime
from fastapi import FastAPI
from tenacity import retry, stop_after_attempt, wait_random


app = FastAPI()


def custom_before_log(retry_state):
    logger = retry_state.kwargs["logger"]
    logger.info(f"Attempt: {retry_state.attempt_number}")


@retry(stop = stop_after_attempt(3), wait = wait_random(1, 2), before = custom_before_log, reraise = True)
def do_something(logger):
    if np.random.uniform() >= 0.7:
        raise Exception("Something went wrong!")


class DummyModelPipeline:

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return "I am a dummy model pipeline"


@serve.deployment(
    health_check_period_s = 30, # trigger check_health method every 30 seconds
    # health_check_timeout_s = 30,
)
class DummyShapPipeline:

    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.logger = logging.getLogger("ray.serve")

        # import atexit
        # atexit.register(self.write_to_file) # TODO: this does not work

    def write_to_file(self):
        do_something(logger = self.logger)      
        self.logger.info(self.name)
        time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        filepath = f'./{time}.txt'
        with open(filepath, "w") as f:
            f.write(time + " " + self.name)
        return "Write to file successfully"
    
    def check_health(self):
        self.write_to_file()

    def __del__(self):
        self.write_to_file()

    # def __ray_terminate__(self): # TODO: this does not work
    #     self.write_to_file()
    #     super().__ray_terminate__()
        

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