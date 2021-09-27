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

    def update(self, move_x_amount: float) -> None:
        self.rect.x = self.rect.x + move_x_amount
        if self.rect.x <= 0:
            self.kill()
