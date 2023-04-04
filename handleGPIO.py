import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep             # delay  

listOfAvailableGPIO = {4,5,6,12,13,16,17,18,19,20,21,22,23,24,25,26,27}


def initGPIO():
    GPIO.setmode(GPIO.BCM)

def initPin(pin):
    GPIO.setup(pin, GPIO.OUT)

def setLedStatus(pin, status):
    print(pin)
    print(status)
    if (status == "on"):
        GPIO.output(pin, GPIO.HIGH)
    else:
        GPIO.output(pin, GPIO.LOW)
    #return status

def getLedStatus(pin):
    if GPIO.input(pin):  
        return "on"
    else:
        return "off"

def validateGPIO(pin):
    if (pin in listOfAvailableGPIO):
        print('pin is ok')
        return True
    else:
        print('pin is not allowed')
        return False
    
def initSwitches(dict):
    initGPIO()
    keys = dict.keys()
    for key in keys:
        print(key)
        pin = dict[key]["Gpio"]
        print(pin)
        print('----------------------')
        initPin(pin)
        state = setLedStatus(pin,"off")
        dict[key]["State"] = state