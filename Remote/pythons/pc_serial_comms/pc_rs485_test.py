import serial
from time import sleep

port = "COM5"
ser = serial.Serial(port, baudrate=19200, timeout=0)
count = 0
print('INITIATING PC TEST')

while True:
    print('PC receive')
    count = 0
    while count < 300:
        data = ser.read(15)
        if len(data) > 0:
            print(data)
        count += 1
        print(count)
        sleep(0.01)
    count = 0
    print('PC transmit')
    while count < 300:
        ser.write('P'.encode('utf-8'))
        count += 1
        sleep(0.01)

ser.close()