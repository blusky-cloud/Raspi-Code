import RPi.GPIO as GPIO
import time
import os
import subprocess

def button_callback(channel):
	prevState = True #because the button was pushed to get here
	flag = 0
	while prevState:
		buttonState = GPIO.input(buttonPin)
		GPIO.output(ledPin, GPIO.LOW)
		time.sleep(0.25)


	print("Button pushed!")


buttonPin = 20
ledPin = 8
flag = 0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.output(ledPin, GPIO.HIGH)

last_state = True
input_state = True
press_start = time.clock()

GPIO.add_event_detect(buttonPin, GPIO.RISING, callback=button_callback)

GPIO.cleanup()
