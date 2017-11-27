from asyncio import gather, get_event_loop, iscoroutine, iscoroutinefunction, sleep, ensure_future

def forever(futureFactories):
    if iscoroutinefunction(futureFactories):
        futureFactories = [futureFactories]
    async def repeat(futureFactory):
        while True:
            await futureFactory()
    futures = [repeat(futureFactory) for futureFactory in futureFactories]
    complete(futures)

def attempt(future):
    ensure_future(future)

def complete(futures):
    if iscoroutine(futures):
        futures = [futures]
    loop = get_event_loop()
    loop.run_until_complete(gather(*futures))