
import umqtt.simple as simple

#import cockle
#cockle.connect('Kitchen2','c3fnh0ile')
#id = cockle.suffix()

id = 'myid'
uplink = simple.MQTTClient(id, "cefn-artful-thinkpad")

def notify(topic, message):
    print("Topic: {} Message {}".format(topic, message))
uplink.set_callback(notify)

uplink.connect()
uplink.publish(topic='yo',msg='mars',retain=True,qos=1)
uplink.subscribe(topic='hello')
while True:
    uplink.wait_msg()