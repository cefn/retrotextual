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
	hue = 0
	steps = 8
	for pos in range(steps):
		while True:
			if hue * steps < pos:
				hue += 0.01
				print( "{} {} ".format(hue, hue_to_rgb(hue)))
				sleep(0.05)
			color = hue_to_rgb(hue)
			clearPixels(show=False)
			for index in allIndexes:
				if index not in (0, 11):
					setPixel(index, color, show=False)
				else:
					setPixel(index, [color[0], color[2], color[1]], show=False)
			for again in range(10):
				showPixels()
			if hue * steps >= pos:
				break
		sleep(2)


