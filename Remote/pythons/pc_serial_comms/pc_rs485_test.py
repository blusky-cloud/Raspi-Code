import serial
from time import sleep

port = "COM5"
ser = serial.Serial(port, 19200, timeout=1)
count = 0
print('INITIATING PC TEST')

while True:
    print('PC receive')
    while count < 300:
        data = ser.read(15)
        if len(data) > 0:
            print(data)
        count += 1
        sleep(0.01)
    print('PC transmit')
    while count < 300:
        ser.write('P'.encode('utf-8'))
        count += 1
        sleep(0.01)

ser.close()