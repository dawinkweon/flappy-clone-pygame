import pygame
from pygame import display
from PipeContainer import PipeContainer
from Pipe import Pipe

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500
PIPE_START_POS_X = 700
PIPE_WIDTH = 50
PIPE_DISTANCE = 300
PIPE_GAP_HEIGHT = 150

class Colors:
    BackgroundColor = (0,0,0)

def clear_display(game_display):
    game_display.fill(Colors.BackgroundColor)
    
pygame.init()
clock = pygame.time.Clock()
game_display = display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

pipe_container = PipeContainer(WINDOW_WIDTH, WINDOW_HEIGHT, PIPE_WIDTH, PIPE_DISTANCE, PIPE_GAP_HEIGHT)
pipe_container.initialize_pipes(PIPE_START_POS_X)

while True:
    clear_display(game_display)

    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            raise SystemExit

    pipe_container.tick()
    pipe_container.draw(pygame, game_display)

    pygame.display.flip()
    clock.tick(60)