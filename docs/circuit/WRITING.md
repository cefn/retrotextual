Possible strategies

* Use a 5V arduino accepting serial bytes from ESP8266's Serial 1 and passing them on to WS2811
* Change the machine.freq() to overclock, increasing performance of ESP8266
* Use a [special implementation of micropython with 'FastLED' support](https://github.com/aykevl/micropython/blob/modpixel/esp8266/modules/pixels.py) (see [forum post](https://forum.micropython.org/viewtopic.php?t=3749)) 
* Disable interrupts for duration of pixel write as per [this forum thread](https://github.com/micropython/micropython/pull/2211)
* Try esp.neopixel_write(pin, buf, is800khz)
* Use SPI [implementation of Neopixel driver](https://github.com/nickovs/ws2812-SPI)
* Consider 2N7000 Mosfet+diode circuit as alternative
