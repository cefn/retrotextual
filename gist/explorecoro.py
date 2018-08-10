import uasyncio as asyncio
from uos import urandom
def random_uint8():
    return int(urandom(1)[0])


class CancelledException(BaseException):
    pass


class BangException(BaseException):
    pass


async def russian_roulette(bulletPos = None):
    if bulletPos is None:
        bulletPos = random_uint8() % 6
    cylinderPos = 0
    while cylinderPos < 6:
        await asyncio.sleep(random_uint8() / 100)
        print("Bullet {} Cylinder {}. Pulling trigger...".format(bulletPos, cylinderPos))
        if cylinderPos == bulletPos:
            print("...Bang!")
            raise BangException
        else:
            print("...click")
        cylinderPos += 1

numPlayers = 10

loop = asyncio.get_event_loop()

def run():
    coros = []
    for count in range(numPlayers):
        coro = russian_roulette()
        coros.append(coro)
        loop.create_task(coro)

    # keep pulling trigger until a coro bangs
    try:
        loop.run_forever()
    except BangException as e:
        pass

    # dispose of all coros (banged or not)
    for coro in coros:
        try:
            coro.throw(CancelledException)
        except StopIteration: # raised by already stopped coro?
            pass
        except CancelledException: # raised by all others?
            pass

    # help loop tidy up the exceptions
    for coro in coros:
        loop.run_until_complete(coro)

while True:
    print("Players ready")
    run()
    print("Game Over: A player has died")