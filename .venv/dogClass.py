import requests
from requests.auth import HTTPBasicAuth
from time import sleep
import json

ORDER_NUMBER=str(697056)

URL1 = "https://pos.snapscan.io/merchant/api/v1/payments?status=completed&merchantReference=" #for checking payment status
#URL2="https://pos.snapscan.io/qr/"#for creating QR codes
API_KEY = "ef960def-2e4e-41ba-ab28-1efb393d74a4"


Payment_status=False
i=1
while Payment_status==False and i<5:

    i+=1
    response=requests.get(URL1+ORDER_NUMBER,auth = HTTPBasicAuth(API_KEY, "")) # gets payment status from SnapScan
    
    if response.status_code == 200 and len(json.loads(response.content)) > 0:
        
        Snap_response=(json.loads(response.content))[0] #only one payment in list so check first item
        check=(Snap_response['merchantReference'])      # dictionary search for OrderNumber refernce
        
        if check==ORDER_NUMBER:
            Payment_status=True
            print("yay")

            #thirdw= self.root.get_screen('thirdwind') 
            #thirdw.ids.QR.source= 'Payment_Successful.png' #shows sucess png
                
        else:
            pass
    else:
        pass
        sleep(0.5)
        
print(Payment_status)