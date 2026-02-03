import requests
import json

url = "http://0.0.0.0:5000/api/v1/nlp/index/answer/1"
headers = {"Content-Type": "application/json"}
data = {
    "text": "What is the capital of France?",
    "limit": 3
}

try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
