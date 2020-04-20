from Drawable import Drawable
import pygame
from Events import Events

class FlappyBird(Drawable):
    def __init__(self, obs, game_configuration, img):
        super().__init__(obs)
        self.x = game_configuration.bird_start_pos[0]
        self.y = game_configuration.bird_start_pos[1]
        self.width = game_configuration.bird_size[0]
        self.height = game_configuration.bird_size[1]
        self.y_bounds = game_configuration.window_height
        self.img = img
        self.velocity = 0
        self.acceleration = 1
        self.can_flap = True
    
    def do_flap(self):
        if self.can_flap:
            self.velocity = -8

    def do_accelerate(self):
        self.velocity = self.velocity + 0.5 * self.acceleration

    def move(self):
        self.y += self.velocity

    def tick(self):
        self.do_accelerate()
        self.move()

        if self.y + self.height >= self.y_bounds:
            # End game when reaching bottom
            self.y = self.y_bounds - self.height
            self.obs.trigger(Events.GameOver)
        elif self.y <= 0:
            # Zero the velocity when ceiling reached
            self.velocity = 0

    def key_down(self, key_code):
        if (key_code == pygame.K_UP):
            self.do_flap()

    def draw(self, pygame, game_display):
        game_display.blit(self.img, (self.x, self.y))

    def game_over(self):
        self.can_flap = False
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)