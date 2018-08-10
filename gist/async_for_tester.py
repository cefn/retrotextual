import sys

if sys.implementation.name == "cpython":
	import asyncio
elif sys.implementation.name == "micropython":
	import uasyncio as asyncio

async def count(bound=8,delay=0.1):
	for num in range(bound):
		await asyncio.sleep(delay)
		yield num
		
async def aggregate(asyncGenerator):
	resultList = []
	async for num in asyncGenerator:
		resultList.append(num)
	return resultList

loop = asyncio.get_event_loop()
coroCount = count()
coroAggregate = aggregate(coroCount)

if sys.implementation.name == "cpython":
	taskAggregate = loop.create_task(coroAggregate)
	results = loop.run_until_complete(taskAggregate)
elif sys.implementation.name == "micropython":
	results = loop.run_until_complete(coroAggregate)
