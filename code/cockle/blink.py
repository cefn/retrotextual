"""main.py regime to verify board is alive at all"""

from machine import Pin
from time import sleep

p = Pin(2, mode=Pin.OUT)
while True:
    p.value(0) # turn on (LED is reverse biased)
    sleep(1)
    p.value(1) # turn off
    sleep(1)
