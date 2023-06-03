import requests


print(requests.get(
    url = 'http://localhost:8000/model',
    params = {'input_text': 'Hello friend!'}
).json())