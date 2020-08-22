from pygame.sprite import Sprite
from pygame import Surface

from typing import Tuple, Optional


class FlappyBird(Sprite):
    DEFAULT_FLAP_SPEED = -8
    FALL_SPEED = 5
    """ The flappy bird sprite """
    def __init__(self, start_pos: Tuple[int, int], image: Surface):
        """ The constructor

        @param start_pos: the x and y start position
        @param image: the image
        """
        Sprite.__init__(self)
        self._target_y_pos = None
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = start_pos[0]
        self.rect.y = start_pos[1]
        self.velocity = 0
        self.acceleration = 1
        self.can_flap = True
        self.can_move = True

    def __do_accelerate__(self) -> None:
        self.velocity = self.velocity + 0.5 * self.acceleration

    def __move__(self) -> None:
        self.rect.y += self.velocity

    def fall_to_y_pos(self, y_pos: int) -> None:
        """ Causes the bird to fall to given position

        @param y_pos: the y position to fall to
        """
        if self._target_y_pos is None:
            self._target_y_pos = y_pos
            self.velocity = FlappyBird.FALL_SPEED
            self.can_flap = False

    def do_flap(self, velocity: Optional = None) -> None:
        """ Causes the bird to perform a single upward flap

        @param velocity: the flap velocity or None for default flap
        """
        if self.can_flap:
            self.velocity = FlappyBird.DEFAULT_FLAP_SPEED if velocity is None else velocity

    def update(self) -> None:
        # Do not move after reaching target
        if self._target_y_pos is not None and self.rect.bottom >= self._target_y_pos:
            self.can_move = False

        if self.can_move:
            self.__do_accelerate__()
            self.__move__()
