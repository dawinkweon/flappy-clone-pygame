import pygame
from pygame import display
from PipeContainer import PipeContainer
from Pipe import Pipe
from observable import Observable
from Events import Events
from FlappyBird import FlappyBird
from AssetFactory import AssetFactory

class GameConfiguration:
    def __init__(self):
        self.window_width = 1000
        self.window_height = 500
        self.pipe_start_pos = 300
        self.pipe_width = 32
        self.pipe_distance = 300
        self.pipe_gap_height = 150
        self.bird_start_pos = (150,0)
        self.bird_size = (50,35)
        self.map_move_speed = 2.5

class Colors:
    BackgroundColor = (255,255,255)

def game_over():
    print("Game over")

def clear_display(game_display):
    game_display.fill(Colors.BackgroundColor)

game_configuration = GameConfiguration()
    
pygame.init()
clock = pygame.time.Clock()
game_display = display.set_mode((game_configuration.window_width, game_configuration.window_height))
obs = Observable()
obs.once(Events.GameOver, game_over)

asset_factory = AssetFactory()

pipe_container = PipeContainer(obs, asset_factory, game_configuration)

flappy_bird_img = asset_factory.create_flappy_bird_image(game_configuration.bird_size[0], game_configuration.bird_size[1])
flappy_bird = FlappyBird(obs, game_configuration, flappy_bird_img)

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