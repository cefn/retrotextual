import segment.font.default as defaultFont
from color import black

class Display:
    def __init__(self, cols=10, rows=2):
        self.cols = cols
        self.rows = rows
        self.characters = []
        self.fontLookup = defaultFont.lookup
        self.foreground = "black"

    def show(self):
        raise NotImplementedError()

    def clear(self, show=True):
        for character in self.characters:
            character.clear(show=show)

class Character:
    def __init__(self, display):
        self.display = display

    def setForeground(self, color):
        self.foreground = color

    def drawSegment(self, index, color, show=True):
        raise NotImplementedError()

    def drawLetter(self, asciiLetter, color=None, clear=True, show=True):
        if color is None:
            color = self.foreground
        if clear:
            self.clear(show=False)
        fontLookup = self.display.fontLookup
        if asciiLetter in fontLookup:
            litSegments = fontLookup[asciiLetter]
            for index in litSegments:
                self.drawSegment(index, color, show=False)
        if show:
            self.show()

    def clear(self, show=True):
        for index in range(16):
            self.drawSegment(index, black, show=False)
        if show:
            self.show()

    def show(self):
        raise NotImplementedError()