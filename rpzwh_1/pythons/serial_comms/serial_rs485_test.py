import serial
#
port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=3.0)

while True:
    port.write(b"Say something:")
    rcv = port.read(10)
    port.write(b"You sent:" + repr(rcv))
