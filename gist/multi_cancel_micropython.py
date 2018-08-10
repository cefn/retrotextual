import uasyncio as asyncio
import sys

class CancelledException(BaseException):
    pass

async def liver(lifeDelay):
    try:
        while True:
            print("Living....la la la")
            await asyncio.sleep(lifeDelay)
    finally:
        print("living() finished. Aaargh!")

async def killer(killDelay, coroToKill):
    await asyncio.sleep(killDelay)
    try:
        print("Killing...")
        # CancelledError will be raised by below call (uncaught in lifeFactory)
        coroToKill.throw(CancelledException)
    except CancelledException:
        raise # if 'pass' is here then run_until_complete hangs
    finally:
        print("killer() finished")

def run():
    loop = asyncio.get_event_loop()

    lifeCoro = liver(0.5)
    deathCoro = killer(2.0, lifeCoro)

    coros = (lifeCoro, deathCoro)

    try:
        for coro in coros:
            loop.create_task(coro)
        loop.run_until_complete(deathCoro)
    finally:
        for coro in coros:
            try:
                coro.throw(CancelledException)
            except CancelledException:
                pass
        for coro in coros:
            loop.run_until_complete(coro)
        print("run() Finished")
        loop.stop()

while True:
    try:
        run()
    except KeyboardInterrupt:
        raise
    except CancelledException:
        continue
    except BaseException as e:
        sys.print_exception(e)
        raise