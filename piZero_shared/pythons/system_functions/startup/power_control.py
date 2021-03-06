import RPi.GPIO as GPIO
import time
import os
import subprocess

def button_callback(channel):
	buttonState = True #because the button was pushed to get here
	flag = 0
	while buttonState:
		buttonState = GPIO.input(buttonPin)
		GPIO.output(ledPin, GPIO.LOW)
		time.sleep(0.25)
		GPIO.output(ledPin, GPIO.HIGH)
		buttonState = GPIO.input(buttonPin)
		flag += 1
		if buttonState and flag > 8:
			print("SHUTDOWN TEST")
	print("NOT PRESSED LONG ENOUGH")

buttonPin = 22
ledPin = 8

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ledPin, GPIO.OUT)

GPIO.output(ledPin, GPIO.LOW)
time.sleep(1)
GPIO.output(ledPin, GPIO.HIGH)

while True:
	GPIO.add_event_detect(buttonPin, GPIO.RISING, callback=button_callback)
	time.sleep(0.25)

GPIO.cleanup()
