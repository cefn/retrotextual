from cockle import randint
first = (randint(255), randint(255), randint(255))
second = (randint(255), randint(255), randint(255))

# found to be stable with segment strip driven by 74HCT245 Quad Buffer (logic level convertor)

from neoSPI import NeoPixel
from machine import SPI,disable_irq,enable_irq
import time
spi = SPI(1, baudrate=3200000)
pixels = NeoPixel(spi, 12)

while True:
    sec = time.time()
    first = (255,0,0)
    second = (0,255,0)
    while (time.time() - sec) < 5:
        pixels[:6] = first
        pixels[6:] = second
        state = disable_irq()
        pixels.write()
        enable_irq(state)
