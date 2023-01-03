from queue import Empty
import gspread
import json


Project="VartProduct"
Restock_Sheet="Restock_List"
Inventory_Sheet= "Inventory_Status"
Inventory_Loaded=[{'Product':'none','Quantity':0, 'Price':0},
                    {'Product':'none','Quantity':0, 'Price':0},
                    {'Product':'none','Quantity':0, 'Price':0}] #this is to build the vector


def Google_Sheet_Restock(Project,Restock_Sheet,):
    """This used to get inventory from Google sheet,
    this sould only be run once after macine is reloaded"""
    #update the file name if api key is moved
    sa = gspread.service_account(filename="varttest-7608f41c9461.json")
    sh = sa.open(Project)
    wks = sh.worksheet(Restock_Sheet)
    Inventory_Loaded = wks.get_all_records()
    
    with open("Inventory_Loaded.json", "w") as outfile:
        json.dump(Inventory_Loaded, outfile)

#Inventory_Loaded=Google_Sheet_Restock(Project,Restock_Sheet)


def Google_Sheet_Update(Project,Inventory_Sheet,Purchase):
    """This is used to update a Google sheet on purchse status """
    #update the file name if api key is moved
    sa = gspread.service_account(filename="varttest-7608f41c9461.json")
    sh = sa.open(Project)
    wks = sh.worksheet(Inventory_Sheet)
    str_list = list(filter(None, wks.col_values(1)))
    first_open=str(len(str_list)+1)
    for i in range(len(Purchase)):
        wks.update_cell(first_open,i+1, Purchase[i])


        

#Google_Sheet_Update(Project,Inventory_Sheet,Purchase)

Google_Sheet_Restock(Project,Restock_Sheet)

with open('Inventory_Loaded.json', 'r') as openfile:

# Reading from json file
    Inventory_Loaded = json.load(openfile)

Snack1_name= (Inventory_Loaded[0]['Product']) 
Snack6_number=(Inventory_Loaded[5]['Quantity'])
Snack3_price=(Inventory_Loaded[2]['Price'])

print(Snack1_name)
print(Snack6_number)
print(Snack3_price)
