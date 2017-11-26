from display.gui import *
from timing import sleep, complete

display = GraphicsDisplay()

async def scheduleWashes():
    while True:
        for color in ["red", "green", "blue"]:
            for character in display.characters:
                for index in range(16):
                    character.setSegment(index, color, show=False)
            display.show()
            await sleep(0.5)

async def scheduleFlashes():
    while True:
        for color in ["red", "green", "blue"]:
            for character in display.characters[1::2]:
                for index in range(16):
                    character.setSegment(index, color, show=False)
            display.show()
            await sleep(0.1)

complete(scheduleWashes(), scheduleFlashes())