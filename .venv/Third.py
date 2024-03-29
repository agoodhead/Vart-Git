from time import sleep
import trio #used for Async
from kivy.app import async_runTouchApp
from functools import partial
from functools import total_ordering
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.image import AsyncImage,Image
from kivy.core.image import Image as CoreImage
from kivy.uix.progressbar import ProgressBar
import copy
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.properties import ObjectProperty
#from kivymd.app import MDApp
from kivy.network.urlrequest import UrlRequest
from PIL import Image
import requests
from requests.auth import HTTPBasicAuth
from kivy.properties import NumericProperty, StringProperty, DictProperty
from queue import Empty
import gspread
import json
import os

##this stuff is used for SnapScan

URL1 = "https://pos.snapscan.io/merchant/api/v1/payments?status=completed&merchantReference=yay"
URL2="https://pos.snapscan.io/qr/"
API_KEY = "ef960def-2e4e-41ba-ab28-1efb393d74a4"
SNAP_CODE= "-XUZdg74"

# This stuff is used for Google sheets

Project="VartProduct"
Restock_Sheet="Restock_List"
Inventory_Sheet= "Inventory_Status"
Inventory_Loaded=[{'Product':'none','Quantity':0, 'Price':0},
                    {'Product':'none','Quantity':0, 'Price':0},
                    {'Product':'none','Quantity':0, 'Price':0}] #this is to build the vector


def Google_Sheet_Restock(Project,Restock_Sheet,):
    """This used to get inventory from Google sheet,
    this sould only be run once after macine is reloaded"""

    
    if os.path.exists("Inventory_Loaded.json"):
        os.remove("Inventory_Loaded.json")
    else:
        print("The file does not exist") 
    
    #update the file name if api key is moved
    sa = gspread.service_account(filename="varttest-7608f41c9461.json")
    sh = sa.open(Project)
    wks = sh.worksheet(Restock_Sheet)
    Inventory_Loaded = wks.get_all_records()
    
    with open("Inventory_Loaded.json", "w") as outfile:
        json.dump(Inventory_Loaded, outfile)

Google_Sheet_Restock(Project,Restock_Sheet)

with open('Inventory_Loaded.json', 'r') as openfile:

# Reading from json file
    Inventory_Loaded = json.load(openfile)

### Read text file to get inventory

Snack1_name= (Inventory_Loaded[0]['Product']) 
Snack1_number=(Inventory_Loaded[0]['Quantity'])
Snack1_price=(Inventory_Loaded[0]['Price'])
Snack2_name=(Inventory_Loaded[1]['Product'])
Snack2_number=(Inventory_Loaded[1]['Quantity'])
Snack2_price=(Inventory_Loaded[1]['Price'])
Snack3_name=(Inventory_Loaded[2]['Product'])
Snack3_number=(Inventory_Loaded[2]['Quantity'])
Snack3_price=(Inventory_Loaded[2]['Price'])
Snack4_name=(Inventory_Loaded[3]['Product'])
Snack4_number=(Inventory_Loaded[3]['Quantity'])
Snack4_price=(Inventory_Loaded[3]['Price'])
Snack5_name=(Inventory_Loaded[4]['Product'])
Snack5_number=(Inventory_Loaded[4]['Quantity'])
Snack5_price=(Inventory_Loaded[4]['Price'])
Snack6_name=(Inventory_Loaded[5]['Product'])
Snack6_number=(Inventory_Loaded[5]['Quantity'])
Snack6_price=(Inventory_Loaded[5]['Price'])


#this should be saved in Text file incase Pi is turned off. File to be overwritten each time purchase is made
Remaining_stock={Snack1_name:Snack1_number,
                    Snack2_name:Snack2_number,
                    Snack3_name:Snack3_number,
                    Snack4_name:Snack4_number,
                    Snack5_name:Snack5_number,
                    Snack6_name:Snack6_number}

#this is should be checked.!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
Remaining_stock_int={Snack1_name:3,Snack2_name:3,Snack3_name:3,Snack4_name:0,Snack5_name:0,Snack6_name:0}  

Total =0 # starts the prorame with zero 
Cart={} # starts teh programe with nothing in cart


vending_ID=1254 #should be number used to generate qr code
ORDER_NUMBER=str(1) #this will be updated for each purchase and will be included in the Snap QR code
QR_status=False #False untill the QR_code has sucsessfully generated


Builder.load_file('changescreen.kv')

class FirstWindow(Screen):
    pass

class SecondWindow(Screen):
    pass

#    async def Progress(self):
    
#         global QR_status
#         try:
#             i = 0
#             while QR_status==False:
#                 print("Progressbar")
#                 # popup = MyPopup()
#                 # current=popupids.my_progress_bar.value
#                 # current+= 0.02
#                 # popup.ids.my_progress_bar.value=current
#                 i += 1
#                 await trio.sleep(1)
#         except trio.Cancelled as e:
#             print('Wasting time was canceled', e)
#         finally:
#         # when canceled, print that it finished
#             print('Done wasting time')

class RootWidget(ScreenManager):
    pass

class MainApp(App):

    status = NumericProperty()
    result_text = StringProperty()
    result_image = StringProperty()
    headers = DictProperty()

    
    nursery = None
    
    def build(self):

        self.Total=Total

        self.Snack1_name=Snack1_name
        self.Snack2_name=Snack2_name
        self.Snack3_name=Snack3_name
        self.Snack4_name=Snack4_name
        self.Snack5_name=Snack5_name
        self.Snack6_name=Snack6_name
        
        self.Snack1_price=Snack1_price
        self.Snack2_price=Snack2_price
        self.Snack3_price=Snack3_price
        self.Snack4_price=Snack4_price
        self.Snack5_price=Snack5_price
        self.Snack6_price=Snack6_price
    
        self.Snack1_remain=Remaining_stock[Snack1_name]
        self.Snack2_remain=Remaining_stock[Snack2_name]
        self.Snack3_remain=Remaining_stock[Snack3_name]
        self.Snack4_remain=Remaining_stock[Snack4_name]
        self.Snack5_remain=Remaining_stock[Snack5_name]
        self.Snack6_remain=Remaining_stock[Snack6_name]

        return RootWidget()

    def Add_cart(self,snack_name): #
        # adds items to cart
        global Cart
        local= self.root.get_screen('first') #used to assign ids to first screen widgets
        
#self.root.get_screen('Write').ids.input.text

        #update cart dictionary
        Cart[snack_name] = Cart.get(snack_name, 0) + 1
        Cart_print = {x:y for x,y in Cart.items() if y!=0} # removes keys with zero items  before printing on screen

        #need some work to print the cart in a neater way !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
        local.ids.CartID.text=f'Cart: {str(Cart_print)}'

    def Update_total(self,snack_n):
        ## updates total cost
        global Total
        local= self.root.get_screen('first')
        second=self.root.get_screen('second')
       
        price =(next((sub for sub in Inventory_Loaded if sub['Product'] == snack_n), None)["Price"]) #gets price
        Total=Total+price
        local= self.root.get_screen('first')
        local.ids.TotalID.text=f'Total Price: R{Total}.00'
        second.ids.CheckoutTotal.text=f'Total Price: R{Total}.00'
    def Rem(self,snack_name):
        
        global Remaining_stock_int
        global Remaining_stock
        global Snack1_name
        global Snack2_name
        global Snack3_name
        global Snack4_name
        global Snack5_name
        global Snack6_name
        local= self.root.get_screen('first')
        
        Remaining_stock_int[snack_name] = Remaining_stock_int.get(snack_name, 0) -1
        
        Snack1_remain=Remaining_stock_int[Snack1_name]
        Snack2_remain=Remaining_stock_int[Snack2_name]
        Snack3_remain=Remaining_stock_int[Snack3_name]
        Snack4_remain=Remaining_stock_int[Snack4_name]
        Snack5_remain=Remaining_stock_int[Snack5_name]
        Snack6_remain=Remaining_stock_int[Snack6_name]

        local.ids.Snack1_count.text=f'Available: {Snack1_remain}'
        if Snack1_remain==0:
            local.ids.Snack1_but.disabled =True

        local.ids.Snack2_count.text=f'Available: {Snack2_remain}'
        if Snack2_remain==0:
            local.ids.Snack2_but.disabled =True
        
        local.ids.Snack3_count.text=f'Available: {Snack3_remain}'
        if Snack3_remain==0:
            local.ids.Snack3_but.disabled =True

        local.ids.Snack4_count.text=f'Available: {Snack4_remain}'
        if Snack4_remain==0:
            local.ids.Snack4_but.disabled =True

        local.ids.Snack5_count.text=f'Available: {Snack5_remain}'
        if Snack5_remain==0:
            local.ids.Snack5_but.disabled =True

        local.ids.Snack6_count.text=f'Available: {Snack6_remain}'
        if Snack6_remain==0:
            local.ids.Snack6_but.disabled =True

    def Clear_all(self):
        global Cart
        global Total
        global Remaining_stock_int
        global Remaining_stock

        local= self.root.get_screen('first')

        Cart={}
        Total=0
    
        local.ids.CartID.text=f'Cart: {Cart}'
        local.ids.TotalID.text=f'Total Price: R{Total}.00'
        local.ids.NextBut.disabled =True
        
        Remaining_stock_int=copy.deepcopy(Remaining_stock) #should reset the remain stock

        Snack1_remain=Remaining_stock_int[Snack1_name]
        local.ids.Snack1_count.text=f'Available: {Snack1_remain}' 
        Snack2_remain=Remaining_stock_int[Snack2_name]
        local.ids.Snack2_count.text=f'Available: {Snack2_remain}'
        Snack3_remain=Remaining_stock_int[Snack3_name]
        local.ids.Snack3_count.text=f'Available: {Snack3_remain}'
        Snack4_remain=Remaining_stock_int[Snack4_name]
        local.ids.Snack4_count.text=f'Available: {Snack4_remain}'
        Snack5_remain=Remaining_stock_int[Snack5_name]
        local.ids.Snack5_count.text=f'Available: {Snack5_remain}'
        Snack6_remain=Remaining_stock_int[Snack6_name]
        local.ids.Snack6_count.text=f'Available: {Snack6_remain}'

        if Snack1_remain>0:    
            local.ids.Snack1_but.disabled =False
        if Snack2_remain>0:    
            local.ids.Snack2_but.disabled =False
        if Snack3_remain>0:    
            local.ids.Snack3_but.disabled =False
        if Snack4_remain>0:    
            local.ids.Snack4_but.disabled =False
        if Snack5_remain>0:    
            local.ids.Snack5_but.disabled =False
        if Snack6_remain>0:    
            local.ids.Snack6_but.disabled =False

    def Disable_button(self):
        local= self.root.get_screen('first')
        local.ids.NextBut.disabled =False

    def QRcode(self):
    # Creating an instance of QRCode class
        global Total
        global vending_ID
        global QR_status
        global QR_code
        
        if Total>0:
            
            TOTAL=str(Total*100)
            #QR_code=requests.get(URL2+SNAP_CODE+".png?id=Ord"+ORDER_NUMBER+"&amount="+TOTAL+"&snap_code_size=250&strict=true")

            url=URL2+SNAP_CODE+".png?id=Ord"+ORDER_NUMBER+"&amount="+TOTAL+"&snap_code_size=250&strict=true"

            QR_code=UrlRequest(url,on_success=self.Pass_image,on_failure=self.Fail_image)
            
            # #"https://pos.snapscan.io/qr/-XUZdg74.png?id=Ord123&amount=1000&snap_code_size=125"
            # if QR_code.status_code == 200:
            #     with open("SnapScanQR.png", "wb") as f:
            #         f.write(QR_code.content)
            #         QR_status=True
            # else:
            #     print("noooooo")
            #     #print(QR_code.status_code)
            #     QR_status=False

    def Pass_image(self, req, result):

        headers = req.resp_headers
        content_type = headers.get('content-type', headers.get('Content-Type'))
        if content_type.startswith('image/'):
            fn = 'SnapScanQR.{}'.format(content_type.split('/')[1])
            with open(fn, 'wb') as f:
                f.write(result)
            self.result_image = fn
        else:
            if isinstance(result, dict):
                self.result_text = json.dumps(result, indent=2)
            else:
                self.result_text = result
        self.status = req.resp_status
        self.headers = headers
       
        # with open("SnapScanQR.png", "wb") as f:
        #     f.write(QR_code.content)
        #     QR_status=True

        second= self.root.get_screen('second')
        second.ids.QR.source= 'SnapScanQR.png'
        
    def Fail_image(self):
        pass

    # async def app_func(self):
    #     '''trio needs to run a function, so this is it. '''

    #     async with trio.open_nursery() as nursery:
    #         '''In trio you create a nursery, in which you schedule async
    #         functions to be run by the nursery simultaneously as tasks.
    #         This will run all two methods starting in random order
    #         asynchronously and then block until they are finished or canceled
    #         at the `with` level. '''
    #         self.nursery = nursery

    # async def run_wrapper():
    #             # trio needs to be set so that it'll be used for the event loop
    #     await self.async_run(async_lib='trio')
    #         print('App done')
    #         nursery.cancel_scope.cancel()

    #         nursery.start_soon(run_wrapper)
    #         nursery.start_soon(self.Progress) 
        
    
                        
    # async def Progress(self):
    #     global QR_status
    #     try:
    #         i = 0
    #         while QR_status==False:
    #             print("Progressbar")
    #             popup = Factory.MyPopup()
    #             current=popup.ids.my_progress_bar.value
    #             current+= 0.02
    #             popup.ids.my_progress_bar.value=current
    #             i += 1
    #             await trio.sleep(5)
    #     except trio.Cancelled as e:
    #         print('Wasting time was canceled', e)
    #     finally:
    #     # when canceled, print that it finished
    #         print('Done wasting time')



if __name__ == '__main__':
    
    MainApp().run()
    
    # trio.run(TestApp().app_func)
