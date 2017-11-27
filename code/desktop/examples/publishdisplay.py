from mqtt.hb import Link
from display.mqtt import MqttSenderDisplay
from examples.hellofade import run
from time import sleep

link = Link()
display = MqttSenderDisplay(link)
run(display)
