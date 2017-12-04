from neoSPI import NeoPixel
from machine import SPI
from utime import ticks_ms, ticks_diff
import gc
from uasyncio import get_event_loop, sleep, sleep_ms
from mqtt_as import MQTTClient, config
from config import config

loop = get_event_loop()

SERVER = '10.42.0.1'
characterIndex = 0
numSegments = 16
segmentSize = 1
numPixels = numSegments * segmentSize

spi = SPI(1, baudrate=3200000)
pixels = NeoPixel(spi, numPixels)

drawPeriodMs = 50 # 20fps

lastDrawnMs = None
drawTask = None

def draw():
    pixels.write()

async def delayedDraw():
    '''Prevents drawing too often'''
    global lastDrawnMs
    if lastDrawnMs is not None:
        waitMs = drawPeriodMs - ticks_diff(ticks_ms(), lastDrawnMs)
        if waitMs >= 0:
            await sleep_ms(waitMs)
    draw()
    lastDrawnMs = ticks_ms()


def lazyScheduleDraw():
    '''Schedules draw if one is not already pending'''
    global drawTask
    if drawTask == None:
        drawTask = loop.create_task(delayedDraw())


async def handleWifiState(state):
    global outages
    if state:
        print('We are connected to broker.')
    else:
        outages += 1
        print('WiFi or broker is down.')
    await sleep(1000)


async def handleConnection(client):
    await client.subscribe("{}/+".format(characterIndex), 1) # TODO consider QOS0


def handleMessage(topic, msg):
    try:
        print("msg has type {}".format(type(msg)))
        folder,entry = topic.split('/')
        if int(folder) == characterIndex:
            try:
                #TODO may need no translation?
                color = msg
                # populate the block of pixels matching the segment with the same color
                segmentIndex = int(entry)
                startPixel = segmentIndex * segmentSize
                endPixel = startPixel + segmentSize
                pixels[startPixel:endPixel] = msg
                lazyScheduleDraw()
            except ValueError:
                # in the future, handle special entities: color, clear
                pass
        else:
            print("Received unexpected topic")
    finally:
        gc.collect()  # dispose of prior color


async def launchClient(client):
    try:
        await client.connect()
    except OSError:
        print('Connection failed.')
        return
    n = 0
    while True:
        await sleep(5)
        print('publish', n)
        # If WiFi is down the following will pause for the duration.
        await client.publish('result', '{} repubs: {} outages: {}'.format(n, client.REPUB_COUNT, outages), qos=1)
        n += 1


# Define configuration
config['server'] = SERVER
config['subs_cb'] = handleMessage
config['wifi_coro'] = handleWifiState
config['connect_coro'] = handleConnection
config['will'] = ('result', 'Goodbye cruel world!', False, 0)
config['keepalive'] = 120


MQTTClient.DEBUG = True  # Optional
client = MQTTClient(config)
try:
    loop.run_until_complete(launchClient(client))
finally:  # Prevent LmacRxBlk:1 errors.
    client.close()