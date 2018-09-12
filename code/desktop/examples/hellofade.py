from timing import *
from color import *
from pangram import examples
from textwrap import wrap
import random

fadeWidth = 3
defaultFadeOnDelay = 0.1
defaultOnDelay = 0.5
defaultOffDelay = 0.5

def getBrightness(index, zeroBrightnessIndex):
    fadePosition = zeroBrightnessIndex - index
    if fadePosition <= 0:  # ahead of the curve, don't light
        return 0
    elif fadePosition <= fadeWidth:  # in the curve, light progressively
        return fadePosition / fadeWidth
    else:  # behind the curve, fully lit
        return 1

async def scheduleLines(display, line1, line2, color, fadeDelay=defaultFadeOnDelay, showDelay=defaultOnDelay):
    display.clear(show=False)

    numCharacters = len(display.characters)
    halfNumCharacters = numCharacters // 2

    # create a brightness curve starting from a zeroIndex
    # todo do not waste time fading empty characters
    for zeroBrightnessIndex in range(len(display.characters) + fadeWidth):

        for index in range(numCharacters):
            if index < len(line1):
                character = display.characters[index]
                character.drawLetter(line1[index],
                                     setBrightness(color, getBrightness(index, zeroBrightnessIndex)),
                                     show=False)
            elif index < halfNumCharacters:
                pass
            elif index < halfNumCharacters + len(line2):
                character = display.characters[index]
                character.drawLetter(line2[index - halfNumCharacters],
                                     setBrightness(color, getBrightness(index, zeroBrightnessIndex)),
                                     show=False)
            else:
                pass

        display.show()
        await sleep(fadeDelay)

    await sleep(showDelay)

async def scheduleMessage(display, message):
    color = hue_to_rgb(random.random())
    numCharacters = len(display.characters)
    lines = wrap(message, numCharacters //2)
    if len(lines) % 2 != 0:
        lines.append("")  # empty line makes them an even number
    for pos in range(0, len(lines), 2):
        await scheduleLines(display, lines[pos], lines[pos + 1], color)


async def schedulePangrams(display):
    for mode in [0]: # range(2): # previously went through upper, mixed and lower case
        for pangram in examples:
            if mode == 0:
                pangram = pangram.upper()
            elif mode == 1:
                pangram = pangram
            else:
                pangram = pangram.lower()
            await scheduleMessage(display, pangram)
            display.clear()
            await sleep(defaultOffDelay)


def run(display):
    async def render():
        return await schedulePangrams(display)
    forever(render)

if __name__ == "__main__":
    from display.gui import GraphicsDisplay
    run(GraphicsDisplay())
