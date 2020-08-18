import pygame
from pygame.sprite import Sprite
from Events import Events

class FlappyBird(Sprite):
    def __init__(self, start_pos, image, game_configuration):
        Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = start_pos[0]
        self.rect.y = start_pos[1]
        self.game_configuration = game_configuration
        self.velocity = 0
        self.acceleration = 1
        self.can_flap = True
        self.can_move = True
    
    def do_flap(self):
        if self.can_flap:
            self.velocity = -8

    def do_accelerate(self):
        self.velocity = self.velocity + 0.5 * self.acceleration

    def move(self):
        self.rect.y += self.velocity

    def update(self):
        if self.can_move:
            self.do_accelerate()
            self.move()