import RPi.GPIO as GPIO
import time 
import os
import subprocess
#from subprocess import run
#import sys

buttonPin = 21
blueLED = 16
yellowLED = 12
flag = 0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(blueLED, GPIO.OUT)
GPIO.setup(yellowLED, GPIO.OUT)

last_state = True
input_state = True
press_start = time.clock()

print("   SSH INDICATION ACTIVE")
GPIO.output(blueLED, GPIO.HIGH)
'''
k = 0
while k<100:
    print(time.clock())
    time.sleep(0.1)
    k+=1
'''
while True:
    input_state = GPIO.input(buttonPin)
    
    if(input_state):
        last_state = True

    if (not input_state):
        
        if(last_state == False):
            while flag < 20 and not input_state:
                GPIO.output(blueLED, GPIO.LOW)
                time.sleep(0.1)
                GPIO.output(blueLED, GPIO.HIGH)
                time.sleep(0.1)
                flag += 1
                input_state = GPIO.input(buttonPin)
            if flag > 19:
                print("         SHUTDOWN")
                flag = 0
                os.system('sudo shutdown -h now')

        print("BUTTON PRESSED")
     #   GPIO.output(yellowLED, GPIO.LOW)
     #   GPIO.output(blueLED, GPIO.LOW)
       # time.sleep(3)
        last_state = False
       
    try:
        output2 = subprocess.check_output('last | grep \'still logged in\'', shell=True)
    except:
        #print("error")
        GPIO.output(yellowLED, GPIO.LOW)
    else:
        #print("ssh active")
        #print(output2)
        GPIO.output(yellowLED, GPIO.HIGH)
            
    #GPIO.output(blueLED, GPIO.HIGH)
    #GPIO.output(yellowLED, GPIO.HIGH)
    #GPIO.output(blueLED, GPIO.LOW)
    #GPIO.output(yellowLED, GPIO.LOW)
    time.sleep(1)
    GPIO.output(blueLED, GPIO.HIGH)

GPIO.cleanup()
