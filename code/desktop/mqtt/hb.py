from mqtt import MqttLink
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1, QOS_2

class Link(MqttLink):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.client = None

    async def getClient(self):
        if self.client is None:
            config = {}
            if self.will is not None:
                will = self.will
                config["will"] = {
                "topic":self.will["topic"],
                "message":self.will["message"],
                "qos":will["qos"] if "qos" in will else 1,
                "retain":will["retain"] if "retain" in will else True,
            }
            self.client = MQTTClient(config=config)
            await self.client.connect("mqtt://{}".format(self.broker))
            await self.client.subscribe([ (topic, QOS_1) for topic in self.subscriptions])
        return self.client

    async def receiveMessages(self):
        client = await self.getClient()
        while True:
            message = await client.deliver_message()
            yield (message.topic, message.data)

    async def sendMessage(self, topicBytes, messageBytes, qos=1, retain=True):
        client = await self.getClient()
        return await client.publish(topicBytes, messageBytes, qos, retain)


if __name__ == "__main__":
    '''Relies on there being an MQTT broker like mosquitto running on localhost'''
    link = Link("localhost", ["hello"])
    async def handleMessages():
        async for topic, message in link.receiveMessages():
            print( "{} {}".format(topic, message))
    import timing
    timing.complete(handleMessages())
