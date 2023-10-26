import pytest
import requests

from ray import serve
from app import SentimentAnalysis


@pytest.mark.asyncio
class TestSentimentAnalysisDeployment:

    async def test_predict_missing_input_text(self):
        response = await SentimentAnalysis.func_or_class().predict(input_text = None)
        assert response == {'message': 'Please provide input_text for inference.'}

    async def test_predict_valid_input_text(self):
        response = await SentimentAnalysis.func_or_class().predict(input_text = "happy")
        assert response == {
            "sentiment": {
                "label": "POSITIVE",
                "score": 0.9998753070831299,
            }, 
            "model": "distilbert-base-uncased-finetuned-sst-2-english",
        }


class TestSentimentAnalysisServer:

    def __setup_endpoint(self):
        serve.run(
            SentimentAnalysis.options(ray_actor_options = {"num_cpus": 0}).bind(), 
        )
    
    def test_predict_server_response(self, ray_serve):
        endpoint = f"{ray_serve.root_url}/model/predict"
        self.__setup_endpoint()

        response = requests.post(endpoint, params = {"input_text": ""})
        assert response.status_code == 200
        assert response.json() == {'message': 'Please provide input_text for inference.'}

        response = requests.post(endpoint, params = {"input_text": "happy"})
        assert response.status_code == 200
        assert response.json() == {
            "sentiment": {
                "label": "POSITIVE",
                "score": 0.9998753070831299,
            }, 
            "model": "distilbert-base-uncased-finetuned-sst-2-english",
        }