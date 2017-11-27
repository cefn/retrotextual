from display.mqtt import MqttMonitor
from timing import complete, sleep


monitor = MqttMonitor()

async def periodicDraw():
    while True:
        await sleep(0.1)
        monitor.guiDisplay.show()

messageCoro = monitor.handleMessages()
drawCoro = periodicDraw()
complete([messageCoro, drawCoro])
