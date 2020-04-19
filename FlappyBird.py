from Drawable import Drawable
import pygame
from Events import Events

class FlappyBird(Drawable):
    DrawColor = (133,133,133)
    def __init__(self, obs, x, y, width, height, y_bounds):
        super().__init__(obs)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.y_bounds = y_bounds
        self.velocity = 0
        self.acceleration = 1
        self.can_move = True
    
    def do_flap(self):
        self.velocity = -8

    def do_accelerate(self):
        self.velocity = self.velocity + 0.5 * self.acceleration

    def move(self):
        self.y += self.velocity

    def tick(self):
        if self.can_move:
            self.do_accelerate()
            self.move()

        if self.y + self.height >= self.y_bounds:
            # End game when reaching bottom
            self.y = self.y_bounds - self.height
            self.can_move = False
            self.obs.trigger(Events.GameOver)
        elif self.y <= 0:
            # Zero the velocity when ceiling reached
            self.velocity = 0

    def key_down(self, key_code):
        if (key_code == pygame.K_UP):
            self.do_flap()

    def draw(self, pygame, game_display):
        pygame.draw.rect(game_display, FlappyBird.DrawColor, pygame.Rect(self.x, self.y, self.width, self.height))

