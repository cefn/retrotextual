from display.mqtt import MqttMonitor
from timing import complete, sleep

delay = 0.2 # should be 0.0 excepting case where CPU shared with animator and broker?

def run(host=None):
	monitor = MqttMonitor(host)

	async def periodicDraw():
		while True:
			await sleep(delay)
			monitor.guiDisplay.show()

	messageCoro = monitor.handleMessages()
	drawCoro = periodicDraw()
	complete([messageCoro, drawCoro])

if __name__=="__main__":
	run('localhost')
#	run('10.42.0.1')
