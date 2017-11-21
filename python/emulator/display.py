from graphics import GraphWin, Point, Polygon
from numpy import array as arr
import math
import asyncio

segmentWidth = 150          # how fat the segments are
shortSegmentLength = 803    # the length of horizontal/vertical segments
longSegmentLength = 905     # the length of diagonal segments
rootTwo = math.sqrt(2)      # useful mathematical constant

# half of the above values (avoids * 0.5 everywhere)
halfSegmentWidth = segmentWidth * 0.5
halfShortSegmentLength = shortSegmentLength * 0.5
halfLongSegmentLength = longSegmentLength * 0.5
halfRootTwo = rootTwo * 0.5

spacing = 30        # the spacing between segments
diagonalSpacing = spacing * halfRootTwo # the spacing where diagonal points meet (spacing at 45 degree angle)

scale = 0.05        # the scale to transfer mm into pixels

def createSegmentPolygon(center, length, degrees):
    halfSegmentLength = length * 0.5
    radians = math.radians(degrees)
    xComponent = arr([math.cos(radians),math.sin(radians)])
    yComponent = arr([math.sin(radians),-math.cos(radians)])
    vertices = []
    # left point
    vertex = center - (xComponent * halfSegmentLength)
    vertices.append(vertex)
    # begin upper long side
    vertex = vertex + (xComponent * halfSegmentWidth) + (yComponent * halfSegmentWidth)
    vertices.append(vertex)
    # end upper long side
    vertex = vertex + (xComponent * (length - segmentWidth))
    vertices.append(vertex)
    # right point
    vertex = vertex + (xComponent * halfSegmentWidth) + (yComponent * -halfSegmentWidth)
    vertices.append(vertex)
    # begin lower long side
    vertex = vertex + (xComponent * -halfSegmentWidth) + (yComponent * -halfSegmentWidth)
    vertices.append(vertex)
    # end lower long side
    vertex = vertex + (xComponent * -(length - segmentWidth))
    vertices.append(vertex)
    return Polygon([Point(arr[0] * scale, arr[1] * scale) for arr in vertices])

windowWidth = 1024
windowHeight = 768
window = GraphWin("Retrotextual", windowWidth, windowHeight, autoflush=False)

# radius includes single imaginary spacing gap around the character and interior diagonal spacing between segments
characterRadius = shortSegmentLength + halfSegmentWidth + spacing + diagonalSpacing
characterDiameter = characterRadius * 2

lineHeight = characterDiameter + characterRadius

characterCenter = arr([characterRadius, lineHeight])

characters = []
for characterRow in range(2):
    for characterCol in range(10):
        character = []
        # segment 0
        segmentCenter = characterCenter + arr([-halfShortSegmentLength, -(diagonalSpacing + shortSegmentLength)])
        segmentLength = shortSegmentLength
        segmentDegrees = 0
        character.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
        # segment 1
        segmentCenter = characterCenter + arr([halfShortSegmentLength, -(diagonalSpacing + shortSegmentLength)])
        segmentLength = shortSegmentLength
        segmentDegrees = 0
        character.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
        # segment 2
        segmentCenter = characterCenter + arr([- (diagonalSpacing + shortSegmentLength), -halfShortSegmentLength])
        segmentLength = shortSegmentLength
        segmentDegrees = 90
        character.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
        # segment 3
        segmentCenter = characterCenter + arr([-(diagonalSpacing + halfShortSegmentLength),-halfShortSegmentLength])
        segmentLength = shortSegmentLength
        segmentDegrees = 45
        character.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
        # segment 4
        segmentCenter = characterCenter + arr([0,-halfShortSegmentLength])
        segmentLength = shortSegmentLength
        segmentDegrees = 90
        character.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
        # segment 5
        segmentCenter = characterCenter + arr([diagonalSpacing + halfShortSegmentLength,-halfShortSegmentLength])
        segmentLength = shortSegmentLength
        segmentDegrees = -45
        character.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
        # segment 6
        segmentCenter = characterCenter + arr([diagonalSpacing + shortSegmentLength, -halfShortSegmentLength])
        segmentLength = shortSegmentLength
        segmentDegrees = 90
        character.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
        # segment 7
        segmentCenter = characterCenter + arr([-halfShortSegmentLength, 0])
        segmentLength = shortSegmentLength
        segmentDegrees = 0
        character.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
        # segment 8
        segmentCenter = characterCenter + arr([halfShortSegmentLength, 0])
        segmentLength = shortSegmentLength
        segmentDegrees = 0
        character.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
        # segment 9
        segmentCenter = characterCenter + arr([- (diagonalSpacing + shortSegmentLength), halfShortSegmentLength])
        segmentLength = shortSegmentLength
        segmentDegrees = 90
        character.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
        # segment 10
        segmentCenter = characterCenter + arr([-(diagonalSpacing + halfShortSegmentLength),halfShortSegmentLength])
        segmentLength = shortSegmentLength
        segmentDegrees = -45
        character.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
        # segment 11
        segmentCenter = characterCenter + arr([0,halfShortSegmentLength])
        segmentLength = shortSegmentLength
        segmentDegrees = 90
        character.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
        # segment 12
        segmentCenter = characterCenter + arr([diagonalSpacing + halfShortSegmentLength,halfShortSegmentLength])
        segmentLength = shortSegmentLength
        segmentDegrees = 45
        character.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
        # segment 13
        segmentCenter = characterCenter + arr([diagonalSpacing + shortSegmentLength, halfShortSegmentLength])
        segmentLength = shortSegmentLength
        segmentDegrees = 90
        character.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
        # segment 14
        segmentCenter = characterCenter + arr([-halfShortSegmentLength, diagonalSpacing + shortSegmentLength])
        segmentLength = shortSegmentLength
        segmentDegrees = 0
        character.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
        # segment 15
        segmentCenter = characterCenter + arr([halfShortSegmentLength, diagonalSpacing + shortSegmentLength])
        segmentLength = shortSegmentLength
        segmentDegrees = 0
        character.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
        # add to character list
        characters.append(character)
        # move horizontal
        characterCenter += arr([characterDiameter, 0])    # next character
    # move vertical
    characterCenter += arr([0, lineHeight])        # line feed
    characterCenter[0] = characterRadius                  # carriage return

def generateColorSequence():
    while True:
        for color in ["red", "green", "blue"]:
            yield color

colorSequence = generateColorSequence()

def generateFrames():
    while True:
        color = next(colorSequence)
        for character in characters:
            for segment in character:
                segment.undraw()
                segment.setFill(color)
                segment.draw(window)
        window.update()
        yield asyncio.sleep(0.001)

animation = generateFrames()

while True:
    next(animation)
