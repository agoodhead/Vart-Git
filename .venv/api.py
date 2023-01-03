import json
import requests
from requests.auth import HTTPBasicAuth

URL1 = "https://pos.snapscan.io/merchant/api/v1/payments?status=completed&merchantReference=yay"
URL2="https://pos.snapscan.io/qr/"
API_KEY = "ef960def-2e4e-41ba-ab28-1efb393d74a4"
SNAP_CODE= "-XUZdg74"

ORDER_NUMBER=str(1)
TOTAL=str(1950)


QR_code=requests.get(URL2+SNAP_CODE+".png?id=Ord"+ORDER_NUMBER+"&amount="+TOTAL+"&snap_code_size=125&strict=true")

#"https://pos.snapscan.io/qr/-XUZdg74.png?id=Ord123&amount=1000&snap_code_size=125"
if QR_code.status_code == 200:
    with open("SnapScanQR.png", "wb") as f:
        f.write(QR_code.content)
else:
    print(QR_code.status_code)

response = requests.get(URL1, auth = HTTPBasicAuth(API_KEY, ""))

print(response.status_code)
print(json.loads(response.content))
