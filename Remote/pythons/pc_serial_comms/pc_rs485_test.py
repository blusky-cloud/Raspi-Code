import serial
from time import sleep

port = "COM5"
ser = serial.Serial(port, 19200, timeout=1)

while True:
    print("  attempting read from laptop ")
    data = ser.read(15)
    if len(data) > 0:
        print(data)
        ser.write('msg received')

    sleep(4)
    print('not blocked')

ser.close()