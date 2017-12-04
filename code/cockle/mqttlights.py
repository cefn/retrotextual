from neoSPI import NeoPixel
from machine import SPI
from utime import ticks_ms, ticks_diff
import gc
from uasyncio import get_event_loop, sleep, sleep_ms
from mqtt_as import MQTTClient, config
from config import config
import esp
esp.osdebug(False)

loop = get_event_loop()
outages = 0

SERVER = '10.42.0.1'
characterIndex = 0
characterName = str(characterIndex).encode('ascii')
numSegments = 16
segmentSize = 1
numPixels = numSegments * segmentSize

spi = SPI(1, baudrate=3200000)
pixels = NeoPixel(spi, numPixels)

drawPeriodMs = 100 # 20fps

lastDrawnMs = None
drawTask = None

def connect(ssid,auth,timeout=16000):
    from network import WLAN, STA_IF, AP_IF
    global uplink
    uplink = WLAN(STA_IF)
    uplink.active(True)
    uplink.connect(ssid, auth)
    started= ticks_ms()
    while True:
        if uplink.isconnected():
            return True
        else:
            if ticks_diff(ticks_ms(), started) < timeout:
                sleep_ms(100)
                continue
            else:
                return False

def draw():
    pixels.write()

async def delayedDraw():
    '''Prevents drawing too often'''
    global drawTask, lastDrawnMs
    if lastDrawnMs is not None:
        waitMs = drawPeriodMs - ticks_diff(ticks_ms(), lastDrawnMs)
        if waitMs >= 0:
            await sleep_ms(waitMs)
    drawTask = None
    draw()
    lastDrawnMs = ticks_ms()
    gc.collect()

def lazyScheduleDraw():
    '''Schedules draw if one is not already pending'''
    global drawTask
    if drawTask == None:
        drawTask = loop.create_task(delayedDraw())
    else:
        pass


async def handleWifiState(state):
    global outages
    if state:
        print('We are connected to broker.')
    else:
        outages += 1
        print('WiFi or broker is down.')
    await sleep(1000)


async def handleConnection(client):
    await client.subscribe("{}/+".format(characterIndex), 0) # TODO consider QOS0


def handleMessage(topic, msg):
    folder,entry = topic.split(b'/')
    if folder == characterName:
        try:
            # populate the block of pixels matching the segment with the same color
            segmentIndex = int(entry)
            startPixel = segmentIndex * segmentSize
            endPixel = startPixel + segmentSize
            pixels[startPixel:endPixel] = (msg[0],msg[1],msg[2])
            lazyScheduleDraw()
        except ValueError:
            print("Entry not a number")
            # in the future, handle special entities: color, clear
            pass
    else:
        print("Received unexpected topic")


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
        await client.publish('ro', '{} r:{} o:{}'.format(n, client.REPUB_COUNT, outages), qos=0)
        n += 1


# Define configuration
config['ssid'] = 'RetroFloorA' if characterIndex < 10 else 'RetroFloorB'
config['wifi_pw'] = '4lphaT3xt' if characterIndex < 10 else '8ravoT3xt'
config['server'] = SERVER
config['subs_cb'] = handleMessage
config['wifi_coro'] = handleWifiState
config['connect_coro'] = handleConnection
config['will'] = ('result', 'Goodbye cruel world!', False, 0)
config['keepalive'] = 120

connect(config['ssid'], config['wifi_pw'])

MQTTClient.DEBUG = True  # Optional
client = MQTTClient(config)
try:
    loop.run_until_complete(launchClient(client))
finally:  # Prevent LmacRxBlk:1 errors.
    client.close()
