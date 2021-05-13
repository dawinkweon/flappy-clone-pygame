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
MAP_MOVE_SPEED = -2.5

game_settings = GameSettings()
score_count = 0
can_pipe_move = True
is_game_over = False

pygame.init()
clock = pygame.time.Clock()
game_display = display.set_mode((game_settings.window_width, game_settings.window_height))

asset_factory = AssetFactory()
pipe_group = Group()
pipe_gaps = Group()
pipe_generator = PipeGenerator(pipe_group, pipe_gaps, asset_factory, game_settings)

flappy_bird_img = asset_factory.create_flappy_bird_image(BIRD_SIZE)
flappy_bird = FlappyBird(BIRD_START_POS, flappy_bird_img)
flappy_bird_group = GroupSingle(flappy_bird)

bg_img = asset_factory.create_bg(game_settings.window_width, game_settings.window_height)

def handle_game_over():
    global can_pipe_move
    global is_game_over

    if not is_game_over:
        is_game_over = True

        flappy_bird.fall_to_y_pos(game_settings.window_height)
        can_pipe_move = False
        print("Game over. Final score was: " + str(score_count))


def increase_score():
    if is_game_over:
        return

    global score_count
    score_count = score_count + 1
    print("Score is: " + str(score_count))

def is_bird_dead():
    # Game ends when bird collides with pipe
    collided_sprite = sprite.spritecollideany(flappy_bird, pipe_group)
    if collided_sprite is not None:
        return True

    # Bird stops moving when hitting near bottom of screen
    bird_death_pos_y = game_settings.window_height - 20
    if flappy_bird.rect.bottom >= bird_death_pos_y:
        return True

    return False

def has_bird_passed_pipe():
     # Score increments when bird goes through pipe gap
    collided_gaps = sprite.spritecollide(flappy_bird, pipe_gaps, False)
    for collided_gap in collided_gaps:
        if collided_gap.is_collided_for_first_time():
            increase_score()

def update_sprites():
    flappy_bird_group.update()
    pipe_generator.update()
    if can_pipe_move:
        pipe_group.update(MAP_MOVE_SPEED)
        pipe_gaps.update(MAP_MOVE_SPEED)

def draw_sprites():
    flappy_bird_group.draw(game_display)
    pipe_group.draw(game_display)
    pipe_gaps.draw(game_display)

while True:
    # Clear display

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            flappy_bird.do_flap()

    if is_bird_dead():
        handle_game_over()
    elif has_bird_passed_pipe():
        increase_score()

    pygame.Surface.blit(game_display, bg_img, [0,0])
    update_sprites()
    draw_sprites()
    pygame.display.flip()
    clock.tick(60)
