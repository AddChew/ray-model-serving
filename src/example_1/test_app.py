import json
import requests


# url = 'http://localhost:8000/model'
# payload = json.dumps({'input_text': 'Hello friend!'})
# print(requests.get(url = url, data = payload).json())


# # Application level APIs
# # API to retrieve information on all serve applications
# url = 'http://localhost:52365/api/serve/applications/'
# print(requests.get(url = url).json())

# # API to update serve applications
# url = 'http://localhost:52365/api/serve/applications/'
# payload = {
#   "applications": [
#     {
#       "name": "muahahaha",
#       "route_prefix": "/model",
#       "import_path": "app:deployment",
#       "runtime_env": {},
#       "deployments": [
#         {"name": "sentiment-analysis", "num_replicas": 2, "user_config": {"model": "distilbert-base-uncased-finetuned-sst-2-english"}}
#       ]
#     }
#   ]
# }
# print(requests.put(url = url, data = json.dumps(payload)))

# # API to shutdown all applications
# url = 'http://localhost:52365/api/serve/applications/'
# print(requests.delete(url = url))


# TODO: explore the use of update deployments via rest api: https://docs.ray.io/en/latest/serve/api/index.html#v1-rest-api-single-application
# TODO: explore and see if it is possible to update deployments independently, instead of updating all at once when serve deploy is called