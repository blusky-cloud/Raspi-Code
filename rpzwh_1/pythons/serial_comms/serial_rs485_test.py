import serial
from time import sleep
#
port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=3.0)
print('RASPI UART RS485 TEST')

while True:
    print('attempting port write')
    port.write(b"Connection Successful, This is the DCM Transmitting")
    #rcv = port.read(10)
    #port.write(b"You sent:")
    sleep(0.25)