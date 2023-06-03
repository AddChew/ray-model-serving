import json
import requests


url = 'http://localhost:8000/model'
payload = json.dumps({'input_text': 'Hello friend!'})
print(requests.get(url = url, data = payload).json())