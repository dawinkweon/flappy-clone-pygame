import pygame
from pygame import display
from PipeGenerator import PipeGenerator
from Pipe import Pipe
from Events import Events
from FlappyBird import FlappyBird
from AssetFactory import AssetFactory
from pygame import sprite
from pygame.sprite import GroupSingle, Group
from GameConfiguration import GameConfiguration

BACKGROUND_COLOR = (255,255,255)
BIRD_START_POS = (150,0)
BIRD_SIZE = (50,35)

game_configuration = GameConfiguration()
    
pygame.init()
clock = pygame.time.Clock()
game_display = display.set_mode((game_configuration.window_width, game_configuration.window_height))

asset_factory = AssetFactory()
pipe_group = Group()
pipe_generator = PipeGenerator(pipe_group, asset_factory, game_configuration)

flappy_bird_img = asset_factory.create_flappy_bird_image(BIRD_SIZE)
flappy_bird = FlappyBird(BIRD_START_POS, flappy_bird_img)
flappy_bird_group = GroupSingle(flappy_bird)
        
can_pipe_move = True

while True:
    # Clear display
    game_display.fill(BACKGROUND_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP):
                flappy_bird.do_flap()

    pipe_generator.update()

    flappy_bird_group.update()
    flappy_bird_group.draw(game_display)

    if can_pipe_move:
        pipe_group.update()
    pipe_group.draw(game_display)

    # Game ends when bird collides with pipe
    collided_sprite = sprite.spritecollideany(flappy_bird, pipe_group)
    if collided_sprite is not None:
        flappy_bird.fall_to_y_pos(game_configuration.window_height)
        can_pipe_move = False

    # Bird stops moving when hitting near bottom of screen
    bird_death_pos_y = game_configuration.window_height - 20
    if flappy_bird.rect.bottom >= bird_death_pos_y:
        flappy_bird.fall_to_y_pos(game_configuration.window_height)
        can_pipe_move = False

    pygame.display.flip()
    clock.tick(60)