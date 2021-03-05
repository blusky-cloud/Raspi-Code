import serial
from time import sleep

port = "COM5"
ser = serial.Serial(port, baudrate=19200, timeout=0)
count = 0
print('INITIATING PC TEST')

while True:
    print('PC receive')
    while count < 6: #3 second intervals
        data = ser.read(15)
        if len(data) > 0:
            print(data)
        count += 1
        #print(count)
        sleep(0.5)
    sleep(0.5)
    print('PC transmit')
    while count > 0:
        ser.write('P'.encode('utf-8'))
        count -= 1
        sleep(0.5)

ser.close()