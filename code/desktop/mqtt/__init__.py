class MqttLink():

    def __init__(self, broker="localhost", subscriptions=[], will=None):
        '''Subclasses should connect setting the last will and testament,
        configure a one-shot set of subscribed topics and pass any matching
        messages to the messageHandler as topic,message pairs where both are
        bytes objects.'''
        self.broker = broker
        self.subscriptions = subscriptions
        self.will = will

    async def sendMessage(self, topicBytes, messageBytes):
        raise NotImplementedError()

    async def receiveMessages(self):
        raise NotImplementedError()