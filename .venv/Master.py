from queue import Empty
import gspread
import datetime
from datetime import datetime
import RPi.GPIO as GPIO
import time 
import qrcode

Vending_ID="uniquie numberfrom QIT" #vending ID priovied by QIT module
Conversion=0.1  #converion between QIT pulse and Rand
Project="VartProduct"
Restock_Sheet="Restock_List"
Inventory_Sheet= "Inventory_Status"

Inventory_Loaded=[{'Product':'none','Quantity':0, 'Price':0},
                    {'Product':'none','Quantity':0, 'Price':0},
                    {'Product':'none','Quantity':0, 'Price':0}] #this is to build the list of dictionaries to zero just to start
    
Snack1_name= (Inventory_Loaded[0]['Product'])   # setting vending product date to zero just to start
Snack1_number=(Inventory_Loaded[0]['Quantity'])
Snack1_price=(Inventory_Loaded[0]['Price'])
Snack2_name=(Inventory_Loaded[1]['Product'])
Snack2_number=(Inventory_Loaded[1]['Quantity'])
Snack2_price=(Inventory_Loaded[1]['Price'])
Snack3_name=(Inventory_Loaded[2]['Product'])
Snack3_number=(Inventory_Loaded[2]['Quantity'])
Snack3_price=(Inventory_Loaded[2]['Price'])


def Get_time():
    date_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    print("date and time:",date_time)
    return date_time
time=Get_time()

def Google_Sheet_Restock(Project,Restock_Sheet,):
    """This used to get inventory from Google sheet,
    this sould only be run once after macine is reloaded"""
    #update the file name if api key is moved
    sa = gspread.service_account(filename="varttest-778a027ca542.json")
    sh = sa.open(Project)
    wks = sh.worksheet(Restock_Sheet)
    Inventory_Loaded = wks.get_all_records()
    global Snack1_name,Snack1_number,               #making all variables global

    Snack1_name= (Inventory_Loaded[0]['Product'])   # setting vending product from Google sheet
    Snack1_number=(Inventory_Loaded[0]['Quantity'])
    Snack1_price=(Inventory_Loaded[0]['Price'])
    Snack2_name=(Inventory_Loaded[1]['Product'])
    Snack2_number=(Inventory_Loaded[1]['Quantity'])
    Snack2_price=(Inventory_Loaded[1]['Price'])
    Snack3_name=(Inventory_Loaded[2]['Product'])
    Snack3_number=(Inventory_Loaded[2]['Quantity'])
    Snack3_price=(Inventory_Loaded[2]['Price'])

Dischage =False #Discharge is used to check if items can be discharged

global Pulse # puls is the internal Rand count
Pulse = 0
def IncreasePulse(channel):
    # Count pulse for payment
    global Pulse
    Pulse += 1

GPIO.setmode(GPIO.BCM)

GPIO.setup(2, GPIO.IN)# pin2 will check for rising signal from QIT device payment pulse
GPIO.add_event_detect(2, GPIO.RISING, callback=IncreasePulse)# Count pulses from GIT device

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Link button from grnd to pin 23 
GPIO.add_event_detect(23, GPIO.Falling,callback=Google_Sheet_Restock, bouncetime=200)#iInterupt thread, the Google_Sheet_Restock function will run

GPIO.cleanup()

def QRcode(total,vending_ID):
    # Creating an instance of QRCode class
    qr = qrcode.QRCode(version = 1,box_size = 10,border = 5)
    qr.add_data(total,vending_ID)
    qr.make(fit = True)
    img = qr.make_image(fill_color = 'black', back_color = 'white')
    img.save('MyQRcode.png')

#Google_Sheet_Restock(Project,Restock_Sheet)
    
def Google_Sheet_Update(Project,Inventory_Sheet,Purchase):
    """This is used to update a Google sheet on purchse status """
    #update the file name if api key is moved
    sa = gspread.service_account(filename="varttest-778a027ca542.json")
    sh = sa.open(Project)
    wks = sh.worksheet(Inventory_Sheet)
    str_list = list(filter(None, wks.col_values(1)))
    first_open=str(len(str_list)+1)
    for i in range(len(Purchase)):
        wks.update_cell(first_open,i+1, Purchase[i])

#Google_Sheet_Update(Project,Inventory_Sheet,Purchase)

#this the main loop that will run forever!!!
while True:
    
    Cart=[]
    Total=0
    

#load back button
# cart buttton   
#load available items to GUI
#button with snack name and price
#button with avalable number

#When button is pressed add Snack to cart and add price to total
    Snack1_In_Cart=0 #number of snack 1 in Cart
    Snack2_In_Cart=0
    Snack3_In_Cart=0

#Loop to add names and price to cart and total

#Cart= creat list with snack names appended
#Total=

    if total>=0 and the pay button is pressed a QRcode is generated

    QRcode(Total,vending_ID)

#display QRcode

#start 60 second timer to check for pulse counter

    t_end = time.time() + 60*1
    while time.time() < t_end:
        if pulse*conversion=>Total         
        Discharge=True
        break
    
    if Discharge =True
        
        #discharge Cart using coil or Uarm
        
        Google_Sheet_Update(Project,Inventory_Sheet, Purchase)#to be updated when purchase happens