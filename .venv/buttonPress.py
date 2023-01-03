
import RPi.GPIO as GPIO
import time 

GPIO.setmode(GPIO.BCM)

def whenbutton(channel)
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    GPIO.add_event_detect(23, GPIO.Falling,callback=whenbutton, bouncetime=200)

    GPIO.cleanup()