from time import sleep
from machine import Pin
from cockle import pins,randint
from ws2811 import *

num_pixels = 20
pins[2].init(mode=Pin.OUT)
startPixels(pin=pins[2], num=num_pixels, order=RBG)
allIndexes = range(num_pixels)
clearPixels()

while True:
    color = [randint(256),randint(256),randint(256)]
    for index in allIndexes:
        setPixel(index, color)
    sleep(1)
    clearPixels()
    sleep(1)
    color = white
    for index in allIndexes:
        setPixel(index, color)
    sleep(1)
    clearPixels()
    sleep(1)
