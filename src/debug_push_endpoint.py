import requests
import json
import time

# Use 5001 to avoid conflict if user has 5000 open
url = "http://127.0.0.1:5001/api/v1/nlp/index/push/1"
headers = {"Content-Type": "application/json"}
data = {
    "do_reset": 1
}

print(f"Testing push endpoint at {url}...")
try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
