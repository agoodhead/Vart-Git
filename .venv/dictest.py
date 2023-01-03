Inventory_Loaded=[{'Product':'kitkat','Quantity':3, 'Price':12},
                    {'Product':'barone','Quantity':3, 'Price':10},
                    {'Product':'cherry','Quantity':3, 'Price':10},
                    {'Product':'apple','Quantity':3, 'Price':10},
                    {'Product':'grape','Quantity':3, 'Price':10},
                    {'Product':'poo','Quantity':3, 'Price':10}]


class test:
 
    def __init__(self, breed):

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
                    Snack6_name:Snack6_number,}
   
    # Class Variable
    animal = 'dog'
 
    # The init method or constructor
    def __init__(self, breed):
 
        # Instance Variable
        self.breed = breed
 
    # Adds an instance variable
    def setColor(self, args):
        self.color = color
 
    # Retrieves instance variable
    def getColor(self):
        return self.color
 


# Driver Code
Rodger = Dog("pug")
Rodger.setColor("brown")
print(Rodger.getColor())