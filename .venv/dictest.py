import json

import requests
from requests.auth import HTTPBasicAuth

URL = "https://pos.snapscan.io/merchant/api/v1/payments"
API_KEY = "ef960def-2e4e-41ba-ab28-1efb393d74a4"
response = requests.get(URL, auth = HTTPBasicAuth(API_KEY, ""))

print(response.status_code)
print(json.loads(response.content))
