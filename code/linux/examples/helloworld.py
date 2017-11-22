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
            character.clear(update=False)
        for index,letter in enumerate("HELLO"):
            display.characters[index].drawLetter(letter, color, update=False)

        for index,letter in enumerate("WORLD"):
            display.characters[index + 10].drawLetter(letter, color, update=False)

        display.update()

        await asyncio.sleep(0.5)

washSchedule = scheduleWashes()

loop = asyncio.get_event_loop()
loop.run_until_complete(washSchedule)
