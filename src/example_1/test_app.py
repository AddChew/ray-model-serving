import json
import requests


# url = 'http://localhost:8000/model'
# payload = json.dumps({'input_text': 'Hello friend!'})
# print(requests.get(url = url, data = payload).json())


# # API to retrieve information on all serve applications
# url = 'http://localhost:52365/api/serve/applications/'
# print(requests.get(url = url).json())


# TODO: explore the use of update deployments via rest api: https://docs.ray.io/en/latest/serve/api/index.html#v2-rest-api-multi-application
# TODO: explore and see if it is possible to update deployments independently, instead of updating all at once when serve deploy is called