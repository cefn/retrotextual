from display import *
from display.gui import GraphicsDisplay
from mqtt.hb import Link
from timing import attempt, sleep

# TODO add clear behaviour which resets all segments, rather than lazy-resetting
# TODO understand why Mosquitto's old published values remain after newly launched publishdisplay script should be reset on launch since all newColor values should differ from prevColor, forcing an MQTT message

segmentTopicTemplate = "{}/{}"
segmentPeriod = 0.05


def marshallSegmentTopic(characterIndex, segmentIndex):
    return segmentTopicTemplate.format(characterIndex, segmentIndex)


def unmarshallSegmentTopic(topic):
    characterIndex, segmentIndex = [int(subpath) for subpath in topic.split('/')]
    return characterIndex, segmentIndex


class MqttSenderCharacter(Character):
    def __init__(self, display, characterIndex):
        assert type(display) is MqttSenderDisplay
        super().__init__(display)
        self.characterIndex = characterIndex
        self.prevColors = [None for pos in range(16)]
        self.nextColors = [bytearray(black) for pos in range(16)]

    def drawSegment(self, index, color, show=True):
        self.nextColors[index] = bytearray(color)
        if show:
            self.show()

    def show(self):
        attempt(self.send())

    async def send(self):
        '''Checks per segment if colors have changed, updates MQTT topics with changes to 3-byte color specs'''
        for segmentIndex, nextColor in enumerate(self.nextColors):
            prevColor = self.prevColors[segmentIndex]
            if nextColor != prevColor:
                self.prevColors[segmentIndex] = nextColor
                await self.display.link.sendMessage(marshallSegmentTopic(self.characterIndex, segmentIndex), nextColor)
                await sleep(segmentPeriod)  # ensures an overall limit on segment dispatch rate


class MqttSenderDisplay(Display):
    def __init__(self, link, cols=None, rows=None): # allow superclass to assert default cols, rows
        super().__init__(cols, rows)
        self.link = link
        for characterIndex in range(self.cols * self.rows):
            self.characters.append(MqttSenderCharacter(self, characterIndex))

    def show(self):
        attempt(self.send())

    async def send(self):
        for character in self.characters:
            await character.send()


class MqttMonitor():
    def __init__(self, host=None):
        if host is not None:
            self.host = host
        else:
            self.host = "localhost"

        self.guiDisplay = GraphicsDisplay()
        self.subscriptions = []
        for characterIndex, guiCharacter in enumerate(self.guiDisplay.characters):
            for segmentIndex in range(16):
                self.subscriptions.append(marshallSegmentTopic(characterIndex, segmentIndex))


    async def handleMessages(self):
        link = Link(self.host, self.subscriptions)
        async for topic, message in link.receiveMessages():
            characterIndex, segmentIndex = unmarshallSegmentTopic(topic)
            self.guiDisplay.characters[characterIndex].drawSegment(segmentIndex, message, show=False)
