import pytest

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



# @serve.deployment(name = 'sentiment-analysis', route_prefix = '/model1', num_replicas = 1, user_config = {"model": DEFAULT_MODEL})
# @serve.ingress(app)
# class SentimentAnalysis:

#     def __init__(self):
#         # Code in __init__ will only run once in each replica on startup
#         # Normally, will load the model here
#         self.model = DEFAULT_MODEL
#         self._classifier = pipeline(task = 'sentiment-analysis', model = self.model)

#     @app.post("/predict")
#     async def predict(self, input_text: str) -> Dict:
#         # payload = await request.json()
#         # input_text = payload.get('input_text')
#         if input_text:
#             return {
#                 'sentiment': self._classifier(input_text)[0],
#                 'model': self.model,
#             }
#         return {'message': 'Please provide input_text for inference.'}