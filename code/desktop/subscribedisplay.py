from display.mqtt import MqttMonitor
from timing import complete, sleep


def run(host=None):
	monitor = MqttMonitor(host)

	async def periodicDraw():
		while True:
			await sleep(0.1)
			monitor.guiDisplay.show()

	messageCoro = monitor.handleMessages()
	drawCoro = periodicDraw()
	complete([messageCoro, drawCoro])

if __name__=="__main__":
	run('localhost')
#	run('10.42.0.1')