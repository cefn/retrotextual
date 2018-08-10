import uasyncio as asyncio
#platform = "esp8266"
platform = "unix"
if platform == "esp8266":
	from uos import urandom
	def random_uint8():
		return int(urandom(1)[0])
elif platform == "unix":
	import urandom
	def random_uint8():
		return int(urandom.getrandbits(8))	

async def russian_roulette(bulletPos = None):
    if bulletPos is None:
        bulletPos = random_uint8() % 6
    cylinderPos = 0
    while cylinderPos < 6:
        await asyncio.sleep(random_uint8() / 100)
        print("Bullet {} Cylinder {}. Pulling trigger...".format(bulletPos, cylinderPos))
        if cylinderPos == bulletPos:
            print("...Bang!")
            return cylinderPos
        else:
            print("...click")
        cylinderPos += 1

numPlayers = 10

class MultiEventLoop(asyncio.EventLoop):
	def run_until_any(self, coros):
		stopcoros = []
		done = []
		pending = list(coros)
		for coro in coros:
			def stopper(coro):
				yield from coro
				pending.remove(coro)
				done.append(coro)
				yield asyncio.StopLoop(0)
			stopcoro = stopper(coro)
			stopcoros.append(stopcoro)
			self.call_soon(stopcoro)
		self.run_forever()
		for stopcoro in stopcoros:
			asyncio.cancel(stopcoro)
		return done, pending

loop = MultiEventLoop()

def run():
    coros = []
    for count in range(numPlayers):
        coro = russian_roulette()
        coros.append(coro)
        loop.create_task(coro)

	while len(coros) > 0:
		done, pending = loop.run_until_any(coros)
		for coro in done:
			coros.remove(coro)

print("Players ready")
run()
print("Game Over: All players have died")
