import asyncio
import traceback

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
        coroToKill.throw(asyncio.CancelledError)
    except asyncio.CancelledError:
        raise # if 'pass' is here then run_until_complete hangs
    finally:
        print("killer() finished")

def run():
    loop = asyncio.get_event_loop()

    lifeCoro = liver(0.5)
    deathCoro = killer(2.0, lifeCoro)

    coros = (lifeCoro, deathCoro)

    try:
        tasks = [loop.create_task(coro) for coro in coros]
        gatheredTask = asyncio.gather(*tasks)
        loop.run_until_complete(gatheredTask)
    except asyncio.CancelledError:
        try:
            gatheredTask.cancel()
            loop.run_until_complete(gatheredTask)
        finally:
            print("run() Finished")

while True:
    try:
        run()
    except KeyboardInterrupt:
        raise
    except asyncio.CancelledError:
        continue
    except BaseException as e:
        traceback.print_exc()
        raise