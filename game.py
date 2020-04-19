import pygame
from pygame import display
from PipeContainer import PipeContainer
from Pipe import Pipe
from observable import Observable
from Events import Events
from FlappyBird import FlappyBird

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500
PIPE_START_POS_X = 700
PIPE_WIDTH = 50
PIPE_DISTANCE = 300
PIPE_GAP_HEIGHT = 150
BIRD_START_POS = (150,0)
BIRD_SIZE = (50,50)

class Colors:
    BackgroundColor = (0,0,0)

def game_over():
    print("Game over")

def clear_display(game_display):
    game_display.fill(Colors.BackgroundColor)
    
pygame.init()
clock = pygame.time.Clock()
game_display = display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
obs = Observable()
obs.once(Events.GameOver, game_over)

pipe_container = PipeContainer(obs, WINDOW_WIDTH, WINDOW_HEIGHT, PIPE_WIDTH, PIPE_DISTANCE, PIPE_GAP_HEIGHT)
pipe_container.initialize_pipes(PIPE_START_POS_X)

flappy_bird = FlappyBird(obs, pipe_container, BIRD_START_POS[0], BIRD_START_POS[1], BIRD_SIZE[0], BIRD_SIZE[1], WINDOW_HEIGHT)

while True:
    clear_display(game_display)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            obs.trigger(Events.KeyDown, event.key)

    obs.trigger(Events.Tick)
    obs.trigger(Events.Draw, pygame, game_display)

    # End the game when bird collides with the pipes
    pipes_as_rect_list = pipe_container.get_pipes_as_rect_list()
    flappy_bird_rect = flappy_bird.get_rect()
    if flappy_bird_rect.collidelist(pipes_as_rect_list) != -1:
        obs.trigger(Events.GameOver)

    pygame.display.flip()
    clock.tick(60)