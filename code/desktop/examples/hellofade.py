from timing import *
from color import *
from pangram import examples
from textwrap import wrap
import random

fadeWidth = 3
defaultFadeDelay = 0.01
defaultShowDelay = 0.5
defaultBlankDelay = 0.5

def getBrightness(index, zeroBrightnessIndex):
    fadePosition = zeroBrightnessIndex - index
    if fadePosition <= 0:  # ahead of the curve, don't light
        return 0
    elif fadePosition <= fadeWidth:  # in the curve, light progressively
        return fadePosition / fadeWidth
    else:  # behind the curve, fully lit
        return 1

async def scheduleLines(line1, line2, color, fadeDelay=defaultFadeDelay, showDelay=defaultShowDelay):
    display.clear(show=False)

    # create a brightness curve starting from a zeroIndex
    # todo do not waste time fading empty characters
    for zeroBrightnessIndex in range(len(display.characters) + fadeWidth):

        for index in range(20):
            if index < len(line1):
                character = display.characters[index]
                character.drawLetter(line1[index],
                                     setBrightness(color, getBrightness(index, zeroBrightnessIndex)),
                                     show=False)
            elif index < 10:
                pass
            elif index < 10 + len(line2):
                character = display.characters[index]
                character.drawLetter(line2[index - 10],
                                     setBrightness(color, getBrightness(index, zeroBrightnessIndex)),
                                     show=False)
            else:
                pass

        display.show()
        await sleep(fadeDelay)

    await sleep(showDelay)

async def scheduleMessage(message):
    color = hue_to_rgb(random.random())
    lines = wrap(message, 10)
    if len(lines) % 2 != 0:
        lines.append("")  # empty line makes them an even number
    for pos in range(0, len(lines), 2):
        await scheduleLines(lines[pos], lines[pos + 1], color)


async def schedulePangrams():
    for mode in range(2):
        for pangram in examples:
            if mode == 0:
                pangram = pangram.upper()
            elif mode == 1:
                pangram = pangram
            else:
                pangram = pangram.lower()
            await scheduleMessage(pangram)
            display.clear()
            await sleep(defaultBlankDelay)


def render(display):
    forever(schedulePangrams)

if __name__ == "__main__":
    from display.gui import GraphicsDisplay

    display = GraphicsDisplay()
    render(display)