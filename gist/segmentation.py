from time import sleep
from cockle import pins,randint
from ws2811 import *

num_pixels = 8
startPixels(num=20, order=RBG)
allIndexes = range(num_pixels)
clearPixels()

def setSequence(sequence, color, show=True):
    for item in sequence:
        setPixel(item, color, show=show)

map = [
    [3],
    [7],
    [2],
    [0],
    [6],
    [5],
    [8],
    [1],
    [11],
    [18],
    [15],
    [16],
    [10],
    [12],
    [17],
    [13],
]

letter_e = [0,1,2,7,8,9,14,15]
letter_x = [3,5,10,12]
letter_c = [0,1,2,9,14,15]
letter_h = [2,6,7,8,9,13]
letter_a = [0,1,2,6,7,8,9,13]
letter_n = [2,3,6,9,12,13]
letter_g = [0,1,2,8,9,13,14,15]

word = [
    letter_e,
    letter_x,
    letter_c,
    letter_h,
    letter_a,
    letter_n,
    letter_g,
    letter_e,
]

while True:
    color = [randint(256),randint(256),randint(256)]
    for letter in word:
        clearPixels()
        for segment in letter:
            setSequence(map[segment], color, show=False)
        showPixels()
        sleep(0.3)
        clearPixels()
        sleep(0.05)
    sleep(2)