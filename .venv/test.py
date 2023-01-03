from functools import total_ordering
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
#from kivy.properties import StringProperty
from kivy.properties import NumericProperty
import datetime
#import qrcode

#Builder.load_file('MyQRcode.jpg')

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

Cart={}
Remaining_stock_int={Snack1_name:0,Snack2_name:0,Snack3_name:0,Snack4_name:0,Snack5_name:0,Snack6_name:0}
Total =0
Tic=0
vending_ID=1254 #should be number used to generate qr code

class MyGrid(Widget):
       
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
        
    
    #Remaining_stock_int=Remaining_stock
    def Rem(self,snack_name):
       
        #global Remaining_stock
        #global Remaining_stock_int
        #global Snack1_name
        #global Snack2_name
        
        print(Remaining_stock)
        print(Remaining_stock_int)

        #Remaining_stock_int=Remaining_stock

        Remaining_stock_int[snack_name] = Remaining_stock_int.get(snack_name, 0) -1
        
        Snack1_remain=Remaining_stock_int[Snack1_name]
        self.ids.Snack1_count.text=f'Available: {Snack1_remain}'
        if Snack1_remain==0:
            self.ids.Snack1_but.disabled =True


    def Clear_all(self):
        global Cart
        global Total
        global Remaining_stock_int
        global Remaining_stock

        print(Remaining_stock)
        Remaining_stock_int=Remaining_stock
        print(Remaining_stock)
        print(Remaining_stock_int)
    
        Cart={}
        Total=0
        self.ids.CartID.text=f'Cart: {Cart}'
        self.ids.TotalID.text=f'Total Price: R{Total}.00'
        self.ids.NextBut.disabled =True

    def QRcode(self):
    # Creating an instance of QRCode class
        global Total
        global vending_ID
    
        if Total>0:
            qr = qrcode.QRCode(version = 1,box_size = 10,border = 5)
            qr.add_data(Total,vending_ID)
            qr.make(fit = True)
            img = qr.make_image(fill_color = 'black', back_color = 'white')
            img.save('MyQRcode.jpg')
            

    def disable_Button(self):
        
        self.ids.NextBut.disabled =False

class TestApp(App):
    
    def build(self):
       
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
    #Snack2_remain=Remaining_stock[Snack2_name]
    #Snack3_remain=Remaining_stock[Snack3_name]
    #Snack4_remain=Remaining_stock[Snack4_name]
    #Snack5_remain=Remaining_stock[Snack5_name]
    #Snack6_remain=Remaining_stock[Snack6_name]
    
        return MyGrid()

if __name__ == "__main__":

    app = TestApp()
    app.run()

        