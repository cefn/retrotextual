# Logic Level and Data Input for WS2812

This document covers a variety of alternatives for Logic Level and wiring of DIN for WS2812B strips

See http://www.newark.com/pdfs/techarticles/microchip/3_3vto5vAnalogTipsnTricksBrchr.pdf for a good overview of tips and tricks for circuits combining both 3v3 and 5v

## Raise Ground Level

As per 

## Use a Buffer

A 74HCT125 buffer can be used as a unidirectional 3v3 to 5v logic level shifter...
https://electronics.stackexchange.com/a/127610

## Optocoupler

https://electronics.stackexchange.com/a/127615

## Transistor and two resistors

https://electronics.stackexchange.com/a/127652

## Run multiple in parallel

This means updates can reach the 'end' of the chain more rapidly, without implying the need to shift-update all the LEDs in between. Supported by a multi-channel logic level shifter as detailed at https://learn.adafruit.com/neopixel-levelshifter/shifting-levels
