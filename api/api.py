from . import api_bp
import RPi.GPIO as GPIO

led_pin = 26
#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(led_pin, GPIO.OUT)

@api_bp.route('/led/on')
def led_on():
    GPIO.output(led_pin, GPIO.HIGH)
    return 'LED ON'

@api_bp.route('/led/off')
def led_off():
    GPIO.output(led_pin, GPIO.LOW)
    return 'LED OFF'

def initGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(led_pin, GPIO.OUT)
