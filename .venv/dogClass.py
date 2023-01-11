import datetime
from time import sleep

Tic=int(datetime.datetime.now().strftime("%f"))/1000

def TimeOut():   
  global Tic
  Tok= int(datetime.datetime.now().strftime("%f"))/1000
  dt=(Tok-Tic)

  while dt<=10:
    print(dt)
    sleep(2)
    Tok= int(datetime.datetime.now().strftime("%f"))/1000
    dt=Tok-Tic
  else:  
    print("not working")
                  
        
TimeOut()