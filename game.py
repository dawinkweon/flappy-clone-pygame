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


class Game:
    def __init__(self):
        self._settings = GameSettings()
        self.score_count = 0
        self.can_pipe_move = True
        self.is_game_over = False

        pygame.init()
        self.clock = pygame.time.Clock()
        self.game_display = display.set_mode(
            (self._settings.window_width, self._settings.window_height))

        self.asset_factory = AssetFactory()
        self._pipe_group = Group()
        self._pipe_gaps = Group()
        self._pipe_generator = PipeGenerator(
            self._pipe_group, self._pipe_gaps, self.asset_factory, self._settings)

        max_mum_pipes = int(self._settings.window_width
                            / (self._settings.pipe_width + self._settings.pipe_distance))
        self._max_num_pipe_parts = max_mum_pipes * PipeGenerator.NUM_PIPE_PARTS
        self.__initialize_pipes__()

        self.flappy_bird_img = self.asset_factory.create_flappy_bird_image(
            BIRD_SIZE)
        self.flappy_bird = FlappyBird(BIRD_START_POS, self.flappy_bird_img)
        self.flappy_bird_group = GroupSingle(self.flappy_bird)

        self.bg_img = self.asset_factory.create_bg(
            self._settings.window_width, self._settings.window_height)

    def __initialize_pipes__(self):
        first_pipe_index = int(self._settings.pipe_start_pos
                               / (self._settings.pipe_width + self._settings.pipe_distance))

        for i in range(first_pipe_index, self._max_num_pipe_parts):
            pipe_x = i * (self._settings.pipe_width +
                          self._settings.pipe_distance)
            self._pipe_generator.create_pipe(pipe_x)

    def __update_pipes__(self):
        # Create more pipes if there's space
        # Each pipe actually has two parts, top and bottom
        num_sprites_to_add = self._max_num_pipe_parts - len(self._pipe_group.sprites())
        if num_sprites_to_add > 0:
            for _ in range(0, num_sprites_to_add):
                self._pipe_generator.create_pipe() 

    def start(self):
        while True:
            # Clear display
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    self.flappy_bird.do_flap()

            if self.is_bird_dead():
                self.handle_game_over()
            elif self.has_bird_passed_pipe():
                self.increase_score()

            pygame.Surface.blit(self.game_display, self.bg_img, [0, 0])
            self.update_sprites()
            self.draw_sprites()
            pygame.display.flip()
            self.clock.tick(60)

    def handle_game_over(self):
        if not self.is_game_over:
            self.is_game_over = True

            self.flappy_bird.fall_to_y_pos(self._settings.window_height)
            self.can_pipe_move = False
            print("Game over. Final score was: " + str(self.score_count))

    def increase_score(self):
        if self.is_game_over:
            return

        self.score_count = self.score_count + 1
        print("Score is: " + str(self.score_count))

    def is_bird_dead(self):
        # Game ends when bird collides with pipe
        collided_sprite = sprite.spritecollideany(
            self.flappy_bird, self._pipe_group)
        if collided_sprite is not None:
            return True

        # Bird stops moving when hitting near bottom of screen
        bird_death_pos_y = self._settings.window_height - 20
        if self.flappy_bird.rect.bottom >= bird_death_pos_y:
            return True

        return False

    def has_bird_passed_pipe(self):
        # Score increments when bird goes through pipe gap
        collided_gaps = sprite.spritecollide(
            self.flappy_bird, self._pipe_gaps, False)
        for collided_gap in collided_gaps:
            if collided_gap.is_collided_for_first_time():
                self.increase_score()

    def update_sprites(self):
        self.flappy_bird_group.update()
        self.__update_pipes__()
        if self.can_pipe_move:
            self._pipe_group.update(MAP_MOVE_SPEED)
            self._pipe_gaps.update(MAP_MOVE_SPEED)

    def draw_sprites(self):
        self.flappy_bird_group.draw(self.game_display)
        self._pipe_group.draw(self.game_display)
        self._pipe_gaps.draw(self.game_display)


def main():
    game = Game()
    game.start()


if __name__ == "__main__":
    main()
