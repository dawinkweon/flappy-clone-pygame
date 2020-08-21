import pygame
from pygame.sprite import Sprite
from pygame import Surface
from typing import Tuple

class FlappyBird(Sprite):
    def __init__(self, start_pos : Tuple[int,int], image : Surface):
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

    def fall_to_y_pos(self, y_pos) -> None:
        self._target_y_pos = y_pos
        self.velocity = 10
        self.acceleration = 0
        self.can_flap = False

    def do_flap(self) -> None:
        if self.can_flap:
            self.velocity = -8

    def update(self) -> None:
        # Do not move after reaching target
        if self._target_y_pos is not None and self.rect.bottom >= self._target_y_pos:
            self.can_move = False

        if self.can_move:
            self.__do_accelerate__()
            self.__move__()