# retrotextual
Huge 16-segment displays for collaborative visual poetry.

# About

The Retrotextual project was conceived by technical architect and artist Cefn Hoile, and imagined and designed with artists Suzie Cross and Dave Lynch for Leeds town centre. It is now maintained by artist and technician [David Boultbee](https://github.com/davidboultbee/retrotextual)

Installed in the windows of a high-rise tower block are 2mx2m square color-controllable 16 segment displays, allowing the creation of visual poetry using the segments to broadcast letters, numbers and visual animations across the city.

# Implementation

The display is driven using python code, offering RGB control of individual segments, intended to be used as part of animation regimes using [async and await](https://www.youtube.com/watch?v=tSLDcRkgTsY) to control text content and brightness/colors as illustrated by [this colour control example](https://github.com/cefn/retrotextual/blob/master/code/desktop/examples/flashwash.py) in which a repeated sequence of colors is sent to all segments, with a 5 second break between colors, or [this text example](https://github.com/cefn/retrotextual/blob/master/code/desktop/examples/helloworld.py) in which letters are drawn to the display.

The fundamentals of Retrotextual are very simple (setting RGB colors of 16 segments). However, python code is provided for 3 distinct configurations in which Retrotextual animation code can be run;

## Contexts for Retrotextual Code

* __Full simulation__ - in this configuration, color-setting calls are made directly on a local segment model, with colors rendered to drawn segments on a graphical [Tk](https://wiki.python.org/moin/TkInter)  window launched on your desktop. This provides a standalone visual simulation of the Retrotextual display.
* __Protocol simulation__ - in this configuration, color-setting calls are made to a 'headless' segment model which is polled for changes with a configurable frequency. Any changes to colors are dispatched to a MQTT broker using the Retrotextual network protocol. At the same time, a networked visual simulation can be launched, subscribing to the MQTT broker, providing a visual rendering of the broker's published colors.
* __Live deployment__ - in this configuration, color-setting calls are also made to a 'headless' segment model but this time running on a Raspberry Pi and publishing to an MQTT broker also running on the Pi. A python-programmable microcontroller attached to each letter subscribes to MQTT topics for its letter's segments. The microcontrollers are connected via a wifi backbone to the Pi's MQTT broker using a self-contained ethernet network. Here the Pi is the ethernet uplink and DHCP broker for multiple uniquely-named Wifi access points, minimising the number of letters connected to a single access point. The segment colors received over MQTT are relayed over a serial link to an Arduino-compatible display driver, which repeatedly refreshes the WS2811-compatible pixels in between receiving and processing serial updates (a total of 192 pixels, each having 3 RGB LEDs correspond to the 16 segments). In parallel, a visual rendering can be launched, which subscribes to the same broker, offering a useful debugging view of the letter behaviours in real time.

## Retrotextual Network Protocol

The network protocol used to broadcast segment colors is very simple, and is based on the established [MQTT standard](http://mqtt.org/faq), in which byte sequences can be published against string 'topics', separated by forward slashes by a broker on IANA standard port 1883. Each component color (Red, Green, Blue) of a segment can be represented as a color between 0 and 255 inclusive. Over MQTT the RGB color is published as a 3 byte sequence to the topic __character/segment__ where __character__ is numbered from 0 and __segment__ is between 0 and 15 inclusive. Canonically when running simulated on a laptop, the broker is available at __localhost__ and when running live on a Raspberry Pi, the broker is available at __10.42.0.1__ where the Pi acts as both DHCP gateway and MQTT broker. 

## Python-programmable Microcontroller

The Display receiver is ([a NodeMCUv2 running Micropython](https://learn.adafruit.com/building-and-running-micropython-on-the-esp8266/flash-firmware) see also [@VGkits resources](https://vgkits.org/blog/projects/vanguard/)) which provide information and tools for managing these devices. We use the [mqtt_as](https://github.com/peterhinch/micropython-mqtt/tree/master/mqtt_as) module to manage Wifi connectivity and subscriptions.

## Device configuration

For each device to perform its role, some special configuration may be needed. In particular;

* Wifi access point - Display receivers should be configured to connect to the closest Wifi SSID to its deployed location.
* Character Index - Display receivers need to know the character they are wired to, in order to subscribe to the proper segments. 
* RGB color order - Display __drivers__ need configuration information for the layout and color order of the character's segments with the following special cases
	- There are two color orders depending on the pixel vendors.
	- Two triangles in the layout are too far apart to be wired directly together. All except the very first letter to be built have a simplification in which three triangle pixels are chained together. The first letter to be built has 6 extra splices to save a Triangle.

# Code for contexts

This section outlines the python modules, classes and arduino sketches which are good starting points for understanding the three different contexts for Retrotextual animations.  See earlier section _Contexts for Retrotextual Code_ for a summary of each contexts in which Retrotextual animations can run.
 
# Full simulation

By default, running e.g. [flashwash.py](https://github.com/cefn/retrotextual/blob/master/code/desktop/examples/flashwash.py) will configure and launch a GraphicDisplay, in which calls to drawSegment are reflected in a simulated window. To run flashwash against a different implementation of a display, create the display and call `flashwash.run(display)`

Change into the `code/desktop` folder, and follow the [configuration instructions](https://github.com/cefn/retrotextual/blob/master/code/desktop/display/README.md) to install python3 dependencies through pip3 then run e.g.

`python3 -m examples.flashwash`

# Protocol simulation

To cause the segment information to be sent to an MQTT broker instead of displaying it on a Tk Window, create a display.mqtt.MqttSenderDisplay (see [mqtt.py](https://github.com/cefn/retrotextual/blob/master/code/desktop/display/mqtt.py)) in the __code/desktop__ folder

To subscribe to the MQTT topics and show the published colors in a simulated Graphical Window, create a display.mqtt.MqttMonitor (see [mqtt.py](https://github.com/cefn/retrotextual/blob/master/code/desktop/display/mqtt.py).

Example python scripts which configure and launch a protocol broadcast and protocol subscription can be found in [code/desktop/examples/publishdisplay.py](https://github.com/cefn/retrotextual/blob/master/code/desktop/examples/publishdisplay.py) and [code/desktop/examples/subscribedisplay.py](https://github.com/cefn/retrotextual/blob/master/code/desktop/examples/subscribedisplay.py)

# Live deployment

Live deployment is the same as the Protocol simulation, except that ESP8266 microcontrollers (D1 Minis) are each running a differently configured python routine by copying the [mqttlights.py](https://github.com/cefn/retrotextual/blob/master/code/cockle/mqttlights.py) to main.py with the specific modifications needed for its letter. See the section __Device Configuration__ above.

They are connected to 5V Arduino Pro Minis (which have the benefit of minimal voltage regulation and unencumbered serial RX and TX). In turn these are connected to these [Triangular](https://www.aliexpress.com/snapshot/0.html?spm=a2g0s.9042647.6.2.55404c4dO2yLVp&orderId=504902475689252&productId=32799774199) and [rectangular](https://www.aliexpress.com/snapshot/0.html?spm=a2g0s.9042647.6.2.1ad14c4drEic9h&orderId=504786566519252&productId=32706227746) LED pixels which are linked sequentially as 192 pixels, by serially wiring 4 quadrants.

The microcontrollers are connected back to a common DHCP-managed ethernet subnet in the range 10.42.0.x with the Raspberry Pi at 10.42.0.1 via GL-AR150 routers installed with OpenWRT. The router configuration files are [versioned in their own repository](https://github.com/ShrimpingIt/openwrt/tree/master/gl-ar150-clean%2Bretro)

A reconnection workaround should now be in place for the transient connectivity failures experienced between the Wifi nodes and the Raspberry Pi (when 20 were running, this appeared to happen at random to one of the letters each day or so). From short-term testing, this causes cause one letter to be out of communication for a few minutes each day. It is not known what the underlying error is, and it is transient and unrepeatable. It was associated with OS-level logged errors like...

```
LmacRxBlk:1
reconnect
state: 2 -> 0 (0)
scandone
state: 0 -> 2 (b0)
state: 2 -> 3 (0)
state: 3 -> 5 (10)
add 0
aid 1
cnt 
LmacRxBlk:1
LmacRxBlk:1
LmacRxBlk:1
state: 5 -> 2 (2c0)
rm 0
```

Bugs like [this](https://github.com/esp8266/Arduino/issues/50) may give some clue as to the underlying issue, and it may be resolved by building using Micropython or Circuitpython images built against a more recent ESP SDK, however, without being able to recreate the issue, it's hard to know for sure.

## Future Developments

A worthwhile workaround to eliminate Wifi connectivity issues would be to frame the segment information in COBS (Consistent Overhead Byte Stuffing) using an RS485 link, for cases where installing and maintaining physical wiring between individual letters is feasible at the install site. RS485 to UART converters and Twisted pair wire is available as part of the installation hardware.
