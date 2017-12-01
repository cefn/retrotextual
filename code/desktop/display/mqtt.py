from display import *
from display.gui import GraphicsDisplay
from mqtt.hb import Link
from timing import attempt

# TODO add clear behaviour which resets all segments, rather than lazy-resetting
# TODO understand why Mosquitto's old published values remain after newly launched publishdisplay script should be reset on launch since all newColor values should differ from prevColor, forcing an MQTT message

segmentTopicTemplate = "{}/{}"

def marshallSegmentTopic(characterIndex, segmentIndex):
    return segmentTopicTemplate.format(characterIndex,segmentIndex)

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

    # TODO CH try to schedule an MQTT write in a round robin which limits the segment rate (e.g. adds a wait whenever a segment is found to have changed, and awaits the proper time for backoff)
    def show(self):
        '''Checks per segment if colors have changed, updates MQTT topics with changes to 3-byte color specs'''
        for segmentIndex,nextColor in enumerate(self.nextColors):
            prevColor= self.prevColors[segmentIndex]
            if nextColor != prevColor:
                attempt(self.display.link.sendMessage(marshallSegmentTopic(self.characterIndex, segmentIndex), nextColor))
                self.prevColors[segmentIndex] = nextColor

class MqttSenderDisplay(Display):
    def __init__(self, link, cols=10,rows=2):
        super().__init__(cols, rows)
        self.link = link
        for characterIndex in range(cols * rows):
            self.characters.append(MqttSenderCharacter(self, characterIndex))

    def show(self):
        for character in self.characters:
            character.show()

class MqttMonitor():
    def __init__(self):
        self.guiDisplay = GraphicsDisplay()
        self.subscriptions = []
        for characterIndex,guiCharacter in enumerate(self.guiDisplay.characters):
            for segmentIndex in range(16):
                self.subscriptions.append(marshallSegmentTopic(characterIndex, segmentIndex))

    async def handleMessages(self):
        link = Link("localhost", self.subscriptions)
        async for topic, message in link.receiveMessages():
            characterIndex, segmentIndex = unmarshallSegmentTopic(topic)
            self.guiDisplay.characters[characterIndex].drawSegment(segmentIndex, message, show=False)