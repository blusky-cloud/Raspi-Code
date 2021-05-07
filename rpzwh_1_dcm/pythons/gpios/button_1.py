import RPi.GPIO as GPIO
import time 
import os

buttonPin = 21
blueLED = 16
yellowLED = 12

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(blueLED, GPIO.OUT)
GPIO.setup(yellowLED, GPIO.OUT)

last_state = True
input_state = True

print("button active")

while True:
    input_state = GPIO.input(buttonPin)
   
    if (not input_state):
        print("BUTTON PRESSED")
        GPIO.output(blueLED, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(yellowLED, GPIO.HIGH)
        time.sleep(1)
        print("-------------")
    GPIO.output(blueLED, GPIO.LOW)
    GPIO.output(yellowLED, GPIO.LOW)
    time.sleep(0.05)

GPIO.cleanup()
