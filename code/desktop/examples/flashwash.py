from display.gui import *
from color import *
from timing import sleep, forever

async def scheduleWashes(display):
    while True:
        for color in [red, green, blue, yellow, teal, purple, white]:
            for character in display.characters:
                for index in range(16):
                    character.drawSegment(index, color, show=False)
            display.show()
            await sleep(5.0)

async def scheduleFlashes(display):
    while True:
        for color in [red, green, blue, yellow, teal, purple, white]:
            for character in display.characters[1::2]:
                for index in range(16):
                    character.drawSegment(index, color, show=False)
            display.show()
            await sleep(0.1)

def run(display):
    async def render():
        return await scheduleWashes(display)
    forever(render)

if __name__ == "__main__":
    from display.gui import GraphicsDisplay
    run(GraphicsDisplay())
