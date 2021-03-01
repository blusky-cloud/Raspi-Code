import serial
from time import sleep

port = "COM5"
ser = serial.Serial(port, 19200, timeout=None)

while True:
    print("  attempting read from laptop ")
    data = ser.read(9999)
    if len(data) > 0:
        print(data)

    sleep(4)
    print('not blocked')

ser.close()