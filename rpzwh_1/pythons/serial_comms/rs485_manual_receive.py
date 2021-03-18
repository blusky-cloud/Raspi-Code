import serial
import serial.rs485
import os
from gpiozero import LED
from time import sleep
#this is a script to test sniffing of the manual rs485 hat
#listening in on communication between desktop and auto switching dcm
msg = b'  dcm contact msg'
port = '/dev/ttyAMA0'
conn = serial.Serial(port, baudrate=19200, timeout=0)

print('RASPI UART MANUAL SWITCHING HAT RS485 TEST')

Tx_Enable = LED(18)
Tx_Enable.off()
S
while True:
    count = 0
    while count < 6:
        rcv = conn.read(15)
        if len(rcv) > 0:
            print(rcv)
        sleep(0.01)
        count += 1

conn.close()
