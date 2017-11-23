from emulator.graphicsDisplay import *

display = GraphicsDisplay()

def generateColorSequence():
    while True:
        for color in ["red", "green", "blue"]:
            yield color

colorSequence = generateColorSequence()

async def scheduleWashes():
    while True:
        color = next(colorSequence)
        for character in display.characters:
            for index in range(16):
                character.setSegment(index, color, show=False)
        display.show()
        await asyncio.sleep(0.5)

async def scheduleFlashes():
    while True:
        color = next(colorSequence)
        for character in display.characters[1::2]:
            for index in range(16):
                character.setSegment(index, color, show=False)
        display.show()
        await asyncio.sleep(0.1)

washSchedule = scheduleWashes()
flashSchedule = scheduleFlashes()

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(washSchedule, flashSchedule))