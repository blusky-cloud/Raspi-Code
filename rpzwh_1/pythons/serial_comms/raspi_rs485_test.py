import serial
import serial.rs485
import os
from gpiozero import LED
from time import sleep
#
msg = b'  dcm contact msg'
port = '/dev/ttyAMA0'
conn = serial.Serial(port, baudrate=19200)
conn.rs485_mode = serial.rs485.RS485Settings(False, True)

print('RASPI UART RS485 TEST')

Tx_Enable = LED(18)
Tx_Enable.on()

while True:
    rconn.write('test rconn'.encode('utf-8'))
    #conn.write(b"Connection Successful, This is the DCM Transmitting")
    #rcv = port.read(10)
    #port.write(b"You sent:")
    sleep(0.25)