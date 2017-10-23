# Logic Level and Data Input for WS2812

This document covers a variety of alternatives for Logic Level and wiring of DIN for WS2812B strips

See http://www.newark.com/pdfs/techarticles/microchip/3_3vto5vAnalogTipsnTricksBrchr.pdf for a good overview of tips and tricks for circuits combining both 3v3 and 5v

## Raise Ground Level

As per http://www.electrobob.com/ws2812-level-translator/#comment-96422 places the 3v3 range of logic across 0.7 to 4.1v instead.

## Use a Buffer

A 74HCT125 buffer can be used as a unidirectional 3v3 to 5v logic level shifter...
Discussion: https://electronics.stackexchange.com/a/127610
Datasheet: http://www.ti.com/lit/ds/symlink/sn74hc125.pdf
Adafruit related part 1: https://www.adafruit.com/product/1787
Adafruit related part 2: https://www.adafruit.com/product/1779

## Optocoupler

https://electronics.stackexchange.com/a/127615

## Transistor and two resistors

https://electronics.stackexchange.com/a/127652

## Pull-up

http://www.electrobob.com/ws2812-level-translator/#comment-96422

## Run multiple in parallel

This means updates can reach the 'end' of the chain more rapidly, without implying the need to shift-update all the LEDs in between. Supported by a multi-channel logic level shifter as detailed at https://learn.adafruit.com/neopixel-levelshifter/shifting-levels

# Information on timing for the protocol

https://wp.josh.com/2014/05/13/ws2812-neopixels-are-not-so-finicky-once-you-get-to-know-them/

# Information on power estimates

https://learn.adafruit.com/sipping-power-with-neopixels
Esp. commentary on brightness: https://learn.adafruit.com/sipping-power-with-neopixels/insights
