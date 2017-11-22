from machine import Pin,freq,disable_irq,enable_irq
import array
import esp
import time
from ws2811 import *

freq(160000000)
pixelcount = 12
out = Pin(5, mode=Pin.OUT,pull=None, value=0)

red = [255,0,0]
green = [0,255,0]
blue = [0,0,255]

redarray = []
bluearray = []
greenarray = []

for pos in range(pixelcount):
    redarray.extend(hue_to_rgb((0 + (pos/pixelcount)) % 1))
    greenarray.extend(hue_to_rgb((0.33 + (pos/pixelcount)) % 1))
    bluearray.extend(hue_to_rgb((0.66 + (pos/pixelcount)) % 1))

    '''
    if pos == 11:
        redarray.extend([0, 0, 255])
        greenarray.extend([0, 255, 0])
        bluearray.extend([255, 0, 0])
    elif pos == 0:
        redarray.extend([255, 0, 0])
        greenarray.extend([0, 0, 255])
        bluearray.extend([0, 255, 0])
    else: # handle RGB
    '''

redarray = array.array('B', redarray)
bluearray = array.array('B', bluearray)
greenarray = array.array('B', greenarray)

while True:
    for arr in [redarray, bluearray, greenarray]:
        sec = time.time()
        while time.time() == sec:
            state = disable_irq()
            esp.neopixel_write(out, arr, True)
            enable_irq(state)
