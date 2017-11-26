from timing import *
from color import *
from display.gui import GraphicsDisplay
display = GraphicsDisplay()

async def scheduleMessage():
    for color in [red, green, blue]:

        display.clear(show=False)

        for index,letter in enumerate("HELLO"):
            character = display.characters[index]
            character.drawLetter(letter, color, show=False)

        for index,letter in enumerate("WORLD"):
            character = display.characters[index + 10]
            character.drawLetter(letter, color, show=False)

        display.show()

        await sleep(0.5)

forever(scheduleMessage)