import serial
#
port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=3.0)

while True:
    port.write("Say something:")
    rcv = port.read(10)
    port.write("You sent:" + repr(rcv))
