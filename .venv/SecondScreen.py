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
from kivy.uix.image import Image
from kivy.uix.progressbar import ProgressBar
import copy
from kivy.uix.screenmanager import Screen,ScreenManager

class FirstWindow(Screen):
    pass
class SecondWindow(Screen):
    pass
class WindowManager(ScreenManager):
    pass

import json
import requests
from requests.auth import HTTPBasicAuth

URL1 = "https://pos.snapscan.io/merchant/api/v1/payments?status=completed&merchantReference=yay"
URL2="https://pos.snapscan.io/qr/"
API_KEY = "ef960def-2e4e-41ba-ab28-1efb393d74a4"
SNAP_CODE= "-XUZdg74"

ORDER_NUMBER=str(1)

# this will be updated by google sheet
Inventory_Loaded=[{'Product':'kitkat','Quantity':3, 'Price':12},
                    {'Product':'barone','Quantity':3, 'Price':10},
                    {'Product':'cherry','Quantity':3, 'Price':10},
                    {'Product':'apple','Quantity':3, 'Price':10},
                    {'Product':'grape','Quantity':3, 'Price':10},
                    {'Product':'poo','Quantity':3, 'Price':10}]

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

Remaining_stock={Snack1_name:Snack1_number,
                    Snack2_name:Snack2_number,
                    Snack3_name:Snack3_number,
                    Snack4_name:Snack4_number,
                    Snack5_name:Snack5_number,
                    Snack6_name:Snack6_number}


Remaining_stock_int={Snack1_name:3,Snack2_name:3,Snack3_name:3,Snack4_name:0,Snack5_name:0,Snack6_name:0} #this should be updated by Google sheet
Total =0
Cart={}
vending_ID=1254 #should be number used to generate qr code
QR_status=False #False untill the QR_code has sucsessfully generated

kv=Builder.load_file('TwoScreen.kv')

class TestApp(App):
    
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
        return kv
        
    def Update_Total(self,snack_n):
        global Total
       
        price =(next((sub for sub in Inventory_Loaded if sub['Product'] == snack_n), None)["Price"])
        Total=Total+price
        self.ids.TotalID.text=f'Total Price: R{Total}.00'

    def Add_cart(self,snack_name):

        global Cart
        
        #update cart dictionary
        Cart[snack_name] = Cart.get(snack_name, 0) + 1
        Cart_print = {x:y for x,y in Cart.items() if y!=0} # removes keys with zero items before printing
        self.ids.CartID.text=f'Cart: {str(Cart_print)}'
        
    def Rem(self,snack_name):
        
        global Remaining_stock_int
        global Remaining_stock
        global Snack1_name
        global Snack2_name
        global Snack3_name
        global Snack4_name
        global Snack5_name
        global Snack6_name
        
        Remaining_stock_int[snack_name] = Remaining_stock_int.get(snack_name, 0) -1
        
        Snack1_remain=Remaining_stock_int[Snack1_name]
        Snack2_remain=Remaining_stock_int[Snack2_name]
        Snack3_remain=Remaining_stock_int[Snack3_name]
        Snack4_remain=Remaining_stock_int[Snack4_name]
        Snack5_remain=Remaining_stock_int[Snack5_name]
        Snack6_remain=Remaining_stock_int[Snack6_name]

        self.ids.Snack1_count.text=f'Available: {Snack1_remain}'
        if Snack1_remain==0:
            self.ids.Snack1_but.disabled =True

        self.ids.Snack2_count.text=f'Available: {Snack2_remain}'
        if Snack2_remain==0:
            self.ids.Snack2_but.disabled =True
        
        self.ids.Snack3_count.text=f'Available: {Snack3_remain}'
        if Snack3_remain==0:
            self.ids.Snack3_but.disabled =True

        self.ids.Snack4_count.text=f'Available: {Snack4_remain}'
        if Snack4_remain==0:
            self.ids.Snack4_but.disabled =True

        self.ids.Snack5_count.text=f'Available: {Snack5_remain}'
        if Snack5_remain==0:
            self.ids.Snack5_but.disabled =True

        self.ids.Snack6_count.text=f'Available: {Snack6_remain}'
        if Snack6_remain==0:
            self.ids.Snack6_but.disabled =True


    def Clear_all(self):
        global Cart
        global Total
        global Remaining_stock_int
        global Remaining_stock

        Cart={}
        Total=0
    
        self.ids.CartID.text=f'Cart: {Cart}'
        self.ids.TotalID.text=f'Total Price: R{Total}.00'
        self.ids.NextBut.disabled =True
        
        Remaining_stock_int=copy.deepcopy(Remaining_stock) #should reset the remain stock

        Snack1_remain=Remaining_stock_int[Snack1_name]
        self.ids.Snack1_count.text=f'Available: {Snack1_remain}' 
        Snack2_remain=Remaining_stock_int[Snack2_name]
        self.ids.Snack2_count.text=f'Available: {Snack2_remain}'
        Snack3_remain=Remaining_stock_int[Snack3_name]
        self.ids.Snack3_count.text=f'Available: {Snack3_remain}'
        Snack4_remain=Remaining_stock_int[Snack4_name]
        self.ids.Snack4_count.text=f'Available: {Snack4_remain}'
        Snack5_remain=Remaining_stock_int[Snack5_name]
        self.ids.Snack5_count.text=f'Available: {Snack5_remain}'
        Snack6_remain=Remaining_stock_int[Snack6_name]
        self.ids.Snack6_count.text=f'Available: {Snack6_remain}'

        if Snack1_remain>0:    
            self.ids.Snack1_but.disabled =False
        if Snack2_remain>0:    
            self.ids.Snack2_but.disabled =False
        if Snack3_remain>0:    
            self.ids.Snack3_but.disabled =False
        if Snack4_remain>0:    
            self.ids.Snack4_but.disabled =False
        if Snack5_remain>0:    
            self.ids.Snack5_but.disabled =False
        if Snack6_remain>0:    
            self.ids.Snack6_but.disabled =False

    def disable_Button(self):
        self.ids.NextBut.disabled =False


    def QRcode(self):
    # Creating an instance of QRCode class
        global Total
        global vending_ID
        global QR_status
        print("noo")
        # if Total>0:
        #     print("test1")
        #     TOTAL=str(Total*100)
        #     QR_code=requests.get(URL2+SNAP_CODE+".png?id=Ord"+ORDER_NUMBER+"&amount="+TOTAL+"&snap_code_size=250&strict=true")

        #     #"https://pos.snapscan.io/qr/-XUZdg74.png?id=Ord123&amount=1000&snap_code_size=125"
        #     if QR_code.status_code == 200:
        #         with open("SnapScanQR.png", "wb") as f:
        #             f.write(QR_code.content)
        #             QR_status=True
        #     else:
        #         print("noooooo")
        #         #print(QR_code.status_code)
        #         QR_status=False

    async def Progress(self):
        global QR_status
        try:
            i = 0
            while QR_status==False:
                print("Progressbar")
                # popup = MyPopup()
                # current=popupids.my_progress_bar.value
                # current+= 0.02
                # popup.ids.my_progress_bar.value=current
                i += 1
                await trio.sleep(1)
        except trio.Cancelled as e:
            print('Wasting time was canceled', e)
        finally:
        # when canceled, print that it finished
            print('Done wasting time')

    async def app_func(self):
        '''trio needs to run a function, so this is it. '''

        async with trio.open_nursery() as nursery:
            '''In trio you create a nursery, in which you schedule async
            functions to be run by the nursery simultaneously as tasks.
            This will run all two methods starting in random order
            asynchronously and then block until they are finished or canceled
            at the `with` level. '''
            self.nursery = nursery

            async def run_wrapper():
                # trio needs to be set so that it'll be used for the event loop
                await self.async_run(async_lib='trio')
                print('App done')
                nursery.cancel_scope.cancel()

            nursery.start_soon(run_wrapper)
            nursery.start_soon(self.Progress)
                        
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
    trio.run(TestApp().app_func)
