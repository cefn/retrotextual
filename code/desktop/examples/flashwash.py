from display.gui import *
from timing import sleep, forever

async def scheduleWashes(display):
    while True:
        for color in [[255,0,0], [0,255,0], [0,0,255]]:
            for character in display.characters:
                for index in range(16):
                    character.drawSegment(index, color, show=False)
            display.show()
            await sleep(0.5)

async def scheduleFlashes(display):
    while True:
        for color in [(255,0,0), (0,255,0), (0,0,255)]:
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
