#!/usr/bin/env python3
##########################################
# Reader for Aidon energy meter (RJ45)
# used by Skellefteå Kraft
#
# Hardware:
#   Raspberry Pi
#   M-Bus client adapter connected to gpio uart
#
# This reader does not handle multi frame hdlc messages
#
# Olov Lindström
# 220423
##########################################
import serial
from parse import parse

ser=serial.Serial("/dev/ttyAMA0",2400,serial.EIGHTBITS,serial.PARITY_EVEN)

while True:
    # Read until tilde (0x7e)
    data = ser.read_until(expected=b'~')

    # If more than 1 char we are out of synk
    if len(data) != 1:
        continue
    
    # Read at least size part of header
    while len(data) < 3:
        data = data+ser.read_until(expected=b'~')

    # Get frame size
    l = (256*data[1]+data[2])&1023

    # Read until we get the whole frame
    while len(data)<(l+2): 
        data=data+ser.read_until(expected=b'~')

    # Make shure the size of the frame is OK
    if len(data)==(l+2):
        # Parse
        try:
            result = parse(data)
        except Exception as e:
            print("Oops!", e.__class__, "occurred.")
        else:
            #Print results
            print("----------------------------------------------")
            for r in result:
                print(f"{r}={result[r]['value']} {result[r]['unit']}")

