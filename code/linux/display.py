import segment.font.default as defaultFont

class Display:
    def __init__(self, cols=10, rows=2):
        self.cols = cols
        self.rows = rows
        self.characters = []
        self.fontLookup = defaultFont.lookup

class Character:
    def __init__(self, display):
        self.display = display