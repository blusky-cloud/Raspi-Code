import serial
from time import sleep

port = "COM5"
ser = serial.Serial(port, 19200, timeout=1)
count = 0
while True:
    while count < 300:
    #print("  attempting read from laptop ")
        data = ser.read(15)
        print(data)
        count += 1
        sleep(0.01)
    while count < 300:
        #print("  attempting read from laptop ")
        ser.write(b'output')
        count += 1
        sleep(0.01)



        #ser.write('msg received')

    #sleep(4)

ser.close()