import cockle
cockle.connect('Kitchen2','c3fnh0ile')
import umqtt.simple as simple
uplink = simple.MQTTClient(cockle.suffix(), "cefn-artful-thinkpad")

def notify(topic, message):
    print("Topic: {} Message {}".format(topic, message))
uplink.set_callback(notify)

uplink.connect()
uplink.publish(topic='/hello',msg='world',retain=True,qos=1)
uplink.subscribe(topic='mars')
