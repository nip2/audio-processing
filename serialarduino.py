
import serial
import io
import sys
from datetime import datetime

# booleans for program mode switching
ready = False
running = False

# open connection: set serial port and baud rate as needed
serPort = "/dev/cu.usbmodem93964301"
baudRate = 9600
ser = serial.Serial(serPort, baudRate)
sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser))

# wait until connection made and arduino starts sending data
while not ready:
    while ser.inWaiting() == 0:
        pass
    cc=str(ser.readline())
    if cc[2:][:-5] == "start":
        ready = True
        print("start")

# take in data from arduino and write to local file
while ready:
    # name file based on timestamp value before the period
    now = datetime.now()
    ts = datetime.timestamp(now)
    ts = str(ts).rsplit('.',1)[0]
    filename = f'data{ts}.txt'
    original_stdout = sys.stdout

    # record incoming data
    with open(filename, 'w') as f:
        sys.stdout = f
        running = True
        while running:
            # each line has a single value
            cc=str(ser.readline())
            # strip value from input
            ss = cc[2:][:-5]
            # stop at end trasmission
            if ss == "end":
                running = False
                ready = False
            # print each value to file
            else:
                print(ss)
            
        sys.stdout = original_stdout
        print("end")

    ser.close
