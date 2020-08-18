import random
from Pipe import Pipe
import pygame
from pygame.sprite import Group
from AssetFactory import AssetFactory, PipeDirection
from GameConfiguration import GameConfiguration

class PipeContainer:
    # Each pipe has a top and bottom part
    NUM_PIPE_PARTS = 2 
    def __init__(self, asset_factory, game_configuration):
        self.asset_factory = asset_factory
        self.game_configuration = game_configuration
        self.pipe_group = Group()
        self.can_move = True

        self.game_configuration.min_pipe_height = int(self.game_configuration.window_height * 0.1)
        self.max_num_pipes = int(self.game_configuration.window_width / (self.game_configuration.pipe_width + self.game_configuration.pipe_distance)) * PipeContainer.NUM_PIPE_PARTS + 2 # Add 2 for some leeway
        
        self.initialize_pipes()

    def initialize_pipes(self):
        first_pipe_index = int(self.game_configuration.pipe_start_pos / (self.game_configuration.pipe_width + self.game_configuration.pipe_distance))

        for i in range(first_pipe_index, self.max_num_pipes):
            pipe_x = i * (self.game_configuration.pipe_width + self.game_configuration.pipe_distance)
            self.create_pipe(pipe_x)

    def create_pipe(self, pipe_x):
        random_pos = random.randint(self.game_configuration.min_pipe_height, self.game_configuration.window_height - self.game_configuration.min_pipe_height - self.game_configuration.pipe_gap_height)
        top_height = self.game_configuration.window_height - (random_pos + self.game_configuration.pipe_gap_height)
        
        top_pipe = self.create_pipe_part(pipe_x, 0, self.game_configuration.pipe_width, top_height, PipeDirection.Down)
        bottom_pipe = self.create_pipe_part(pipe_x, self.game_configuration.window_height - random_pos, self.game_configuration.pipe_width, random_pos, PipeDirection.Up)

        self.pipe_group.add(top_pipe)
        self.pipe_group.add(bottom_pipe)
        
    def create_pipe_part(self, x, y, width, height, pipe_direction):
        pipe_img = self.asset_factory.create_pipe_image((width, height), pipe_direction)
        return Pipe(x, y, pipe_img, self.game_configuration.map_move_speed)

    def add_pipe_from_end(self):
        last_pipe = self.pipe_group.sprites()[-1]
        new_pipe_x = last_pipe.rect.x + self.game_configuration.pipe_width + self.game_configuration.pipe_distance
        self.create_pipe(new_pipe_x)

    def update(self, surface):
        if self.can_move:
            self.pipe_group.update()
        self.pipe_group.draw(surface)
        
        # Add more pipes if there's space
        # Each pipe actually has two parts, top and bottom
        num_sprites_to_add = self.max_num_pipes - len(self.pipe_group.sprites())
        if (num_sprites_to_add > 0):
            for i in range(num_sprites_to_add):
                self.add_pipe_from_end()