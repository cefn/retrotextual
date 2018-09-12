from display.gui import *
from color import *
from timing import sleep, forever

#colors = [red, green, blue, yellow, teal, purple, white]
colors = [white]
colors = [red, green, blue]

async def scheduleWashes(display):
    while True:
        for color in colors:
            for character in display.characters:
                for index in range(16):
                    character.drawSegment(index, color, show=False)
            display.show()
            await sleep(1.0)

async def scheduleFlashes(display):
    while True:
        for color in colors:
            for character in display.characters[1::2]:
                for index in range(16):
                    character.drawSegment(index, color, show=False)
            display.show()
            await sleep(1.0)

def run(display):
    async def render():
        return await scheduleWashes(display)
    forever(render)

if __name__ == "__main__":
    from display.gui import GraphicsDisplay
    run(GraphicsDisplay())
