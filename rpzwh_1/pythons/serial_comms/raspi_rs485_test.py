import serial
import serial.rs485
import os
from gpiozero import LED
from time import sleep
#
msg = b'  dcm contact msg'
port = '/dev/ttyAMA0'
conn = serial.Serial(port, baudrate=19200, timeout=5)
#conn.rs485_mode = serial.rs485.RS485Settings(False, True)

print('RASPI UART RS485 TEST')

Tx_Enable = LED(18)
Tx_Enable.on()
count = 0
while True:
    print('attempting raspi transmit')
    Tx_Enable.on()
    count = 0
    while count < 300:
        conn.write('R'.encode('utf-8'))
        count += 1
        # conn.write(b"Connection Successful, This is the DCM Transmitting")
        # rcv = conn.read(10)
        # if len(rcv) > 0:
        # print(rcv)
        # port.write(b"You sent:")
        sleep(0.01)

    Tx_Enable.off()
    count = 0
    sleep(0.5)
    print('attempting raspi receive')
    while count < 300:
        rcv = conn.readall()
        if rcv:
            print(rcv)
        sleep(0.01)
        count += 1

conn.close()