import RPi.GPIO as GPIO
import time
import os
import subprocess


print("IDLE - ^c to interrupt, or hold button until LED stops flashing to power down")
buttonPin = 22
ledPin = 8
flag = 0
secs = 0.00 #time
prevSecs = 0.00
buttonPushed = False

def displayIdleClock(idleTime):
	print("Idle for {} minutes".format(idleTime * 2))

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ledPin, GPIO.OUT)

GPIO.output(ledPin, GPIO.LOW)
time.sleep(0.5)
GPIO.output(ledPin, GPIO.HIGH)
time.sleep(1)
GPIO.output(ledPin, GPIO.LOW)
time.sleep(1)
GPIO.output(ledPin, GPIO.HIGH)
time.sleep(1)
GPIO.output(ledPin, GPIO.LOW)
time.sleep(1)
GPIO.output(ledPin, GPIO.HIGH)
time.sleep(1)

while True:
	try:
		print("Loop")
		buttonPushed = GPIO.input(buttonPin)
		flag = 0

		if (secs - prevSecs > 120): #it's been 2 minutes
			displayIdleClock(secs)
			prevSecs = secs

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
		secs += 0.25

	except KeyboardInterrupt:
		print("IDLE OVER")
		break

GPIO.output(ledPin, GPIO.LOW)
GPIO.cleanup()
