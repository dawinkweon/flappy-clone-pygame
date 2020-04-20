class Pipe:
    def __init__(self, x, y, width, height, img):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = img

    def move_left(self, move_amount):
        self.x -= move_amount

    def __str__(self):
        return ("Pipe with x: %s, y: %s, width: %s, height: %s" % (str(self.x), str(self.y), str(self.width), str(self.height)))