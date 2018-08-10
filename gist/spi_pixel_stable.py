# found to be stable with segment strip driven by 74HCT245 Quad Buffer (logic level convertor)

from neoSPI import NeoPixel
from machine import SPI,disable_irq,enable_irq
import time

#pl9823 = 2923076
pl9823 = 2850000
ws2812 = 3200000
spi = SPI(1, baudrate=pl9823)
count = 24
pixels = NeoPixel(spi, count)

halfcount = count // 2

first = (255,0,0)
second = (0,255,0)

while True:
    pixels[:] = first
    state = disable_irq()
    pixels.write()
    enable_irq(state)
    time.sleep(0.01)


