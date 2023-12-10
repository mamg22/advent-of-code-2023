class Grid:
    def __init__(self, width, height, default_value=None):
        self.width = width
        self.height = height
        self.content = [[default_value] * width for _ in range(height)]
    
    def get(self, x, y):
        if x < 0 or x > self.width or y < 0 or y > self.height:
            raise IndexError(f"({x}, {y}) is out of grid area")
        return self.content[y][x]

    def set(self, x, y, value):
        if x < 0 or x > self.width or y < 0 or y > self.height:
            raise IndexError(f"({x}, {y}) is out of grid area")
        self.content[y][x] = value
