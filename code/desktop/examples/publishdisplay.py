from mqtt.hb import Link
from display.mqtt import MqttSenderDisplay
from examples.hellofade import run
#from examples.flashwash import run

link = Link()
display = MqttSenderDisplay(link)
run(display)
