import serial
from time import sleep
#
port = '/dev/ttyAMA0'
conn = serial.Serial(port, baudrate=115200, timeout=0)
print('RASPI UART RS485 TEST')

while True:
    print('attempting port write')
    conn.write(b"Connection Successful, This is the DCM Transmitting")
    #rcv = port.read(10)
    #port.write(b"You sent:")
    sleep(5)