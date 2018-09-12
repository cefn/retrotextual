"""Sends serial frames describing pixels to an Arduino driver board running uartcharacter.ino"""
from neoSPI import NeoPixel
from machine import SPI,freq
from utime import ticks_ms, ticks_diff
import gc
from uasyncio import get_event_loop, sleep_ms
from mqtt_as import MQTTClient, config
from config import config
import esp

esp.osdebug(False)
freq(160000000)

loop = get_event_loop()
outages = 0
lastUpMs = None

SERVER = '10.42.0.1'
characterIndex = 0
characterName = str(characterIndex).encode('ascii')
segmentPattern = "{}/+".format(characterIndex)
livenessTopic = 'node/{}'.format(characterName)
numSegments = 16
segmentSize = 1
numPixels = numSegments * segmentSize

spi = SPI(1, baudrate=3200000)
pixels = NeoPixel(spi, numPixels)

framesPerSecond = 20
drawPeriodMs = 1000 // framesPerSecond
drawNeeded = False

async def launchDrawing():
    while True:
        global drawNeeded
        if drawNeeded:
            pixels.write()
            drawNeeded = False
        await sleep_ms(drawPeriodMs)


def scheduleDraw():
    global drawNeeded
    drawNeeded = True


def connect(ssid, auth, timeout=16000):
    from network import WLAN, STA_IF, AP_IF
    global uplink
    uplink = WLAN(STA_IF)
    uplink.active(True)
    uplink.connect(ssid, auth)
    started = ticks_ms()
    while True:
        if uplink.isconnected():
            return True
        else:
            if ticks_diff(ticks_ms(), started) < timeout:
                sleep_ms(100)
                continue
            else:
                return False

def reportUptime():
    if lastUpMs != None:
        print("Uptime {}ms ".format(ticks_diff(ticks_ms(), lastUpMs)))
    print("{} outages so far".format(outages))

async def handleWifiState(state):
    global outages, lastUpMs
    if state:
        lastUpMs = ticks_ms()
        print('We are connected to broker.')
    else:
        outages += 1
        reportUptime()
        print('WiFi or broker is down.')
        lastUpMs = None
    await sleep_ms(1000)


async def handleConnection(client):
    await client.publish(livenessTopic, b'live', retain=True, qos=1)
    await client.subscribe(segmentPattern, qos=0)


def handleMessage(topic, msg):
    gc.collect()
    folder, entry = topic.split(b'/')
    if folder == characterName:
        try:
            # populate the block of pixels matching the segment with the same color
            segmentIndex = int(entry)
            startPixel = segmentIndex * segmentSize
            endPixel = startPixel + segmentSize
            pixels[startPixel:endPixel] = (msg[0], msg[1], msg[2])
            scheduleDraw()
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
        await sleep_ms(5000)


# Define configuration
config['ssid'] = 'RetroFloorA' if characterIndex < 10 else 'RetroFloorB'
config['wifi_pw'] = '4lphaT3xt' if characterIndex < 10 else '8ravoT3xt'
config['server'] = SERVER
config['subs_cb'] = handleMessage
config['wifi_coro'] = handleWifiState
config['connect_coro'] = handleConnection
config['will'] = (livenessTopic, 'dead', True, 1)
config['keepalive'] = 120

connect(config['ssid'], config['wifi_pw'])

MQTTClient.DEBUG = True  # Optional
client = MQTTClient(config)

# never complete
async def periodicStatus():
    while True:
        await client.publish(livenessTopic, b'live', retain=True, qos=1)
        reportUptime()
        await sleep_ms(10000)
#try:
clientTask = loop.create_task(launchClient(client))
drawTask = loop.create_task(launchDrawing())
loop.run_until_complete(periodicStatus())
#finally:  # Prevent LmacRxBlk:1 errors.
#    client.close()
