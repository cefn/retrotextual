'''Corresponds with serialthru.ino Arduino receiving sketch'''
from time import sleep
from machine import UART
#baud = 9600
baud = 57600
uart = UART(1, baud)  # UART on
#uart.init(baud, bits=8, parity=None, stop=1)
while True:
    uart.write(bytes('yo, mars\n'.encode('ascii')))
