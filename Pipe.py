from pygame.sprite import Sprite
from pygame import Surface


class Pipe(Sprite):
    """ The pipe sprite """
    def __init__(self, x: int, y: int, image: Surface):
        """ The constructor

        @param x: The x position
        @param y: The y position
        @param image: The pipe image
        """
        Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move_horizontally(self, x: float):
        self.rect.x = self.rect.x + x

    def update(self) -> None:
        if self.rect.x <= 0:
            self.kill()
