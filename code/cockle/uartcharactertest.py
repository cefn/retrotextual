import esp
import gc
import sys
from machine import UART, RTC, DEEPSLEEP, freq, deepsleep
from utime import ticks_ms, ticks_diff, sleep_ms as blocking_sleep_ms
from uasyncio import get_event_loop, sleep_ms as async_sleep_ms
from mqtt_as import MQTTClient, config
from config import config
from network import WLAN, STA_IF, AP_IF

homeConfig = dict(
    broker="192.168.1.17",
    ssid="SkyHome",
    auth="c3fnh0ile",
)

mobileConfig = dict(
    broker="192.168.43.58",
    ssid="SkyMobile",
    auth="c3fnh0ile",
)

#debugConfig = mobileConfig
debugConfig = None

MQTTClient.DEBUG = False  # suppress mqtt_as Memory reports

# shutdown 'access point' network interface
downlink = WLAN(AP_IF)
if downlink.active():
    downlink.active(False)

# bring up 'station' network interface
uplink = WLAN(STA_IF)
if not (uplink.active()):
    uplink.active(True)

# prevent certain verbose errors
esp.osdebug(None)
# overclock CPU for speed
freq(160000000)

characterIndex = 1

characterName = str(characterIndex).encode('ascii')
segmentPattern = "{}/+".format(characterIndex)
livenessTopic = 'node/{}'.format(characterName)

if debugConfig is not None:
    ssid = debugConfig['ssid']
    auth = debugConfig['auth']
    broker = debugConfig['broker']
else:
    ssid = 'RetroFloorA' if characterIndex < 10 else 'RetroFloorB'
    auth = '4lphaT3xt' if characterIndex < 10 else '8ravoT3xt'
    broker = '10.42.0.1'

numSegments = 16
segmentSize = 1
numPixels = numSegments * segmentSize
chainMap = (14,11,15,12,13,8,10,1,9,2,0,5,4,7,3,6)

framesPerSecond = 20
drawPeriodMs = 1000 // framesPerSecond
drawNeeded = False

bytesPerPixel = 3
pixelCount = 16
baud = 115200

# Networking and MQTT configuration
config['server'] = broker
config['will'] = (livenessTopic, 'dead', True, 1)
config['keepalive'] = 120

startedMs = ticks_ms()
lastUpMs = None
outages = 0

class UartLights:
    '''Used to write LED color as 3 RGB bytes over a serial link'''
    def __init__(self, pixelCount=16, baud=115200, bytesPerPixel = 3):
        assert pixelCount < 256 # a single byte is used to set the pixelcount
        self.uart = UART(1, baud)
        self.header = bytes([pixelCount])   # set the leading byte to be permanently the pixelCount
        self.buffer = bytearray(pixelCount * bytesPerPixel) # a byte each for red, green, blue
        self.footer = bytes([ord('\n')])    # set the trailing byte to be permanently newline

    def sendColorBytes(self):
        self.uart.write(self.header)
        self.uart.write(self.buffer)
        self.uart.write(self.footer)

lights = UartLights(pixelCount=pixelCount, baud=baud, bytesPerPixel=bytesPerPixel)


async def serviceDrawing():
    global drawNeeded
    while True:
        if drawNeeded:
            lights.sendColorBytes()
            drawNeeded = False
        await async_sleep_ms(drawPeriodMs)


def scheduleDraw():
    global drawNeeded
    drawNeeded = True


def hardreset():

    # configure RTC.ALARM0 to be able to wake the device
    rtc = RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=DEEPSLEEP)

    # set RTC.ALARM0 to fire after 1000 ms (waking the device)
    rtc.alarm(rtc.ALARM0, 1000)

    # put the device to sleep
    deepsleep()


def launchwifi(ssid, auth): # todo make async?
    if not(uplink.isconnected()):
        print(b'Connecting...')
        uplink.connect(ssid, auth)
        for count in range(16):
            if uplink.isconnected():
                print(b'Now connected')
                return True
            else:
                blocking_sleep_ms(1000)
        raise Exception("Uplink not available")
    else:
        print(b'Already connected')
        return True


def printReport():
    uptime = 0
    if lastUpMs != None:
        uptime = ticks_diff(ticks_ms(), lastUpMs) // 1000
    print("Uptime {} s, outages {}".format(uptime, outages))

async def handleBrokerState(connected):
    """Callback registered with mqtt_as handling changes to network"""

    # Currently, simply resets
    if not connected:
        print("Disconnected. Attempt hard reset")
        hardreset()

    #Previously, attempted to track and recover
    """
    global outages, lastUpMs
    if connected:
        lastUpMs = ticks_ms()
        print('We are connected to broker.')
    else:
        outages += 1
        printReport()
        print('WiFi or broker is down.')
        lastUpMs = None
    await async_sleep_ms(1000)

    """


async def publishLiveness(client):
    await client.publish(livenessTopic, b'live', retain=True, qos=1)


async def handleConnection(client):
    await publishLiveness(client)
    await client.subscribe(segmentPattern, qos=0)


def handleMessage(topic, msg):
    # artificially raises an exception after 20 seconds
    """
    if ticks_diff(ticks_ms(), startedMs) > 20000:
        print("Raising exception")
        raise Exception
    """
    gc.collect()
    folder, entry = topic.split(b'/')
    if folder == characterName:
        try:
            # populate the block of pixels matching the segment with the same color
            segmentIndex = chainMap[int(entry)]
            startPixel = segmentIndex * segmentSize
            endPixel = startPixel + segmentSize
            for pixel in range(startPixel, endPixel):
                startByte = pixel * 3
                endByte = startByte + 3
                lights.buffer[startByte:endByte] = msg
            scheduleDraw()
        except ValueError:
            print("Entry not a number")
            # in the future, handle special entities: color, clear
            pass
    else:
        print("Received unexpected topic")


async def serviceMqtt():

    config['wifi_coro'] = handleBrokerState
    config['connect_coro'] = handleConnection
    config['subs_cb'] = handleMessage

    publishPeriod = config['keepalive'] * 1000 // 2

    client = MQTTClient(config)

    try:
        try:
            await client.connect()
            while True:
                await publishLiveness(client)
                printReport()
                await async_sleep_ms(publishPeriod)
        except OSError:
            print('Connection failed.')
            raise
        finally:
            # Prevent LmacRxBlk:1 hang?
            client.close()

    except KeyboardInterrupt:
        raise
    except Exception as e:
        print("Exception in serviceMqtt()")
        sys.print_exception(e)
        hardreset()

loop = get_event_loop()

def service():

    # ensure wifi connection
    launchwifi(ssid, auth)

    mqttCoro = serviceMqtt()
    drawCoro = serviceDrawing()

    loop.create_task(mqttCoro)
    loop.create_task(drawCoro)

    loop.run_until_complete(mqttCoro)

def run():
    try:
        while True:
            try:
                userInterrupt = False
                service()
            except KeyboardInterrupt:
                userInterrupt = True
                break
            except Exception as e: # in future try to handle some exceptions and re-run service()?
                sys.print_exception(e)
                raise
    finally:
        if not userInterrupt:
            hardreset() # handle case of some kind of unexpected (network) failure

if __name__ == "__main__":
    run()