from queue import Empty
import gspread
import datetime
from datetime import datetime

Project="VartProduct"
Restock_Sheet="Restock_List"
Inventory_Sheet= "Inventory_Status"
Inventory_Loaded=[{'Product':'none','Quantity':0, 'Price':0},
                    {'Product':'none','Quantity':0, 'Price':0},
                    {'Product':'none','Quantity':0, 'Price':0}] #this is to built the vector

def Get_time():
   
    date_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    print("date and time:",date_time)
    return date_time
time=Get_time()

def Google_Sheet_Restock(Project,Restock_Sheet,):
    """This used to get inventory from Google sheet,
    this sould only be run once after macine is reloaded"""
    #update the file name if api key is moved
    sa = gspread.service_account(filename="varttest-7608f41c9461.json")
    sh = sa.open(Project)
    wks = sh.worksheet(Restock_Sheet)
    Inventory_Loaded = wks.get_all_records()
    return Inventory_Loaded 

Inventory_Loaded=Google_Sheet_Restock(Project,Restock_Sheet)

print(Inventory_Loaded)

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

#Google_Sheet_Restock(Project,Restock_Sheet)

