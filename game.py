import pygame
from pygame import display
from PipeContainer import PipeContainer
from Pipe import Pipe
from Events import Events
from FlappyBird import FlappyBird
from AssetFactory import AssetFactory
from pygame import sprite
from pygame.sprite import GroupSingle
from GameConfiguration import GameConfiguration

class Colors:
    BackgroundColor = (255,255,255)

def clear_display(game_display):
    game_display.fill(Colors.BackgroundColor)

game_configuration = GameConfiguration()
    
pygame.init()
clock = pygame.time.Clock()
game_display = display.set_mode((game_configuration.window_width, game_configuration.window_height))

asset_factory = AssetFactory()

pipe_container = PipeContainer(asset_factory, game_configuration)

# Bird
bird_start_pos = (150,0)
bird_size = (50,35)

flappy_bird_img = asset_factory.create_flappy_bird_image(bird_size)
flappy_bird = FlappyBird(bird_start_pos, flappy_bird_img, game_configuration)
flappy_bird_group = GroupSingle(flappy_bird)

def handle_key_down(key):
    if (key == pygame.K_UP):
        flappy_bird.do_flap()
        
def handle_game_over():
    global pipe_container
    pipe_container.can_move = False


while True:
    clear_display(game_display)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            handle_key_down(event.key)

    pipe_container.update(game_display)
    flappy_bird_group.update()
    flappy_bird_group.draw(game_display)

    # Game ends when bird collides with pipe
    collided_sprite = sprite.spritecollideany(flappy_bird, pipe_container.pipe_group)
    if collided_sprite is not None:
        flappy_bird.can_flap = False
        pipe_container.can_move = False

    # Bird stops moving when hitting bottom of screen
    if flappy_bird.rect.y - flappy_bird.rect.height >= game_configuration.window_height:
        flappy_bird.rect.y = game_configuration.window_height - flappy_bird.rect.height
        flappy_bird.can_move = False
        pipe_container.can_move = False

    pygame.display.flip()
    clock.tick(60)