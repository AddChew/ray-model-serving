import json
import requests
from access_key import api_key


url = 'http://localhost:8000/model'
headers = {'accessKey': api_key}
payload = json.dumps({'input_text': 'Hello friend!'})
print(requests.post(url = url, headers = headers, data = payload).json())