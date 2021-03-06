import RPi.GPIO as GPIO
import time
import os
import subprocess

print("POWER CONTROL")
buttonPin = 22
ledPin = 8

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ledPin, GPIO.OUT)

GPIO.output(ledPin, GPIO.LOW)
time.sleep(1)
GPIO.output(ledPin, GPIO.HIGH)
buttonPushed = False
flag = 0

while True:
	buttonPushed = GPIO.input(buttonPin)
	flag = 0
	while buttonPushed:
		GPIO.output(ledPin, GPIO.LOW)
		time.sleep(0.12)
		GPIO.output(ledPin, GPIO.HIGH)
		buttonPushed = GPIO.input(buttonPin)
		time.sleep(0.12)
		flag += 1
		if buttonPushed and flag > 8:
			print("SHUTDOWN TEST")
			GPIO.output(ledPin, GPIO.LOW)
			time.sleep(1)

		else:
			print("NOT PRESSED LONG ENOUGH")


	time.sleep(0.25)

GPIO.output(ledPin, GPIO.LOW)
GPIO.cleanup()
