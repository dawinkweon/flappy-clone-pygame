import pygame
from pygame import display
from pygame import sprite
from pygame.sprite import GroupSingle, Group

from GameSettings import GameSettings
from AssetFactory import AssetFactory
from PipeGenerator import PipeGenerator
from FlappyBird import FlappyBird

BACKGROUND_COLOR = (255, 255, 255)
BIRD_START_POS = (150, 0)
BIRD_SIZE = (50, 35)

game_settings = GameSettings()

pygame.init()
clock = pygame.time.Clock()
game_display = display.set_mode((game_settings.window_width, game_settings.window_height))

asset_factory = AssetFactory()
pipe_group = Group()
pipe_generator = PipeGenerator(pipe_group, asset_factory, game_settings)

flappy_bird_img = asset_factory.create_flappy_bird_image(BIRD_SIZE)
flappy_bird = FlappyBird(BIRD_START_POS, flappy_bird_img)
flappy_bird_group = GroupSingle(flappy_bird)

can_pipe_move = True


def __handle_game_over__():
    global can_pipe_move

    flappy_bird.fall_to_y_pos(game_settings.window_height)
    can_pipe_move = False


while True:
    # Clear display
    game_display.fill(BACKGROUND_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
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
        __handle_game_over__()

    # Bird stops moving when hitting near bottom of screen
    bird_death_pos_y = game_settings.window_height - 20
    if flappy_bird.rect.bottom >= bird_death_pos_y:
        __handle_game_over__()

    pygame.display.flip()
    clock.tick(60)
