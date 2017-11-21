from time import sleep

from machine import Pin, freq, disable_irq, enable_irq

from cockle import pins, randint

from ws2811 import *
freq(160000000)

num_pixels = 12

pins[2].init(mode=Pin.OUT)

startPixels(pin=pins[1], num=num_pixels, order=RBG)
allIndexes = range(num_pixels)

clearPixels()


def setAll(color):
    for pos in range(num_pixels):
        if pos not in (0, 11):
            setPixel(pos, color, show=False)
        else:
            setPixel(pos, [color[0], color[2], color[1]], show=False)
    state = disable_irq()
    showPixels()
    enable_irq(state)

while True:
    hue = 0
    steps = 8

    for pos in range(steps):
        while True:
            if hue * steps < pos:
                hue += 0.01
                print("{} {} ".format(hue, hue_to_rgb(hue)))
                sleep(0.05)

            color = hue_to_rgb(hue)
            clearPixels(show=False)

            if hue * steps >= pos:
                break
            showPixels()
        sleep(2)