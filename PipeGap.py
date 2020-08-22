from pygame.sprite import Sprite
from pygame.surface import Surface


class PipeGap(Sprite):
    """ The gap between the pipes """
    def __init__(self, rect):
        """ Constructor for the pipe gap

        @param rect: the pipe gap rect
        """
        Sprite.__init__(self)
        self.rect = rect
        self.image = Surface((rect.width, rect.height))
        self.image.set_alpha(0)
        self._is_collided = False

    def is_collided_for_first_time(self):
        """ Sets the collided flag and checks if colliding for the first time"""
        if not self._is_collided:
            self._is_collided = True
            return True
        return False

    def move_horizontally(self, x: float):
        self.rect.x = self.rect.x + x

    def update(self):
        if self.rect.x <= 0:
            self.kill()