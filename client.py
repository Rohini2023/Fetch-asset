import requests
import json
import os 
from dotenv import load_dotenv
load_dotenv() 

API_TOKEN = os.getenv("API_TOKEN") 

url = "http://localhost:8080/platform-asset-1.0.0/latest/filter/access"

payload = json.dumps({
  "domain": "lremcofc",
  "offset": 1,
  "pageSize": 10
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': API_TOKEN
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)