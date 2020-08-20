import random
from Pipe import Pipe
import pygame
from pygame.sprite import Group
from AssetFactory import AssetFactory, PipeDirection
from GameConfiguration import GameConfiguration

class PipeGenerator:
    # Each pipe has a top and bottom part
    NUM_PIPE_PARTS = 2 
    
    def __init__(self, pipe_group, asset_factory, game_configuration):
        self._asset_factory = asset_factory
        self._game_configuration = game_configuration
        self._pipe_group = pipe_group

        self.can_move = True

        self._min_pipe_height = int(self._game_configuration.window_height * 0.1)
        self._max_num_pipes = int(self._game_configuration.window_width / (self._game_configuration.pipe_width + self._game_configuration.pipe_distance)) * PipeGenerator.NUM_PIPE_PARTS + 2 # Add 2 for some leeway
        
        self.__initialize_pipes__()

    def __initialize_pipes__(self):
        first_pipe_index = int(self._game_configuration.pipe_start_pos / (self._game_configuration.pipe_width + self._game_configuration.pipe_distance))

        for i in range(first_pipe_index, self._max_num_pipes):
            pipe_x = i * (self._game_configuration.pipe_width + self._game_configuration.pipe_distance)
            self.__create_pipe__(pipe_x)

    def __create_pipe__(self, pipe_x):
        random_pos = random.randint(self._min_pipe_height, self._game_configuration.window_height - self._min_pipe_height - self._game_configuration.pipe_gap_height)
        top_height = self._game_configuration.window_height - (random_pos + self._game_configuration.pipe_gap_height)
        
        top_pipe = self.__create_pipe_part__(pipe_x, 0, self._game_configuration.pipe_width, top_height, PipeDirection.Down)
        bottom_pipe = self.__create_pipe_part__(pipe_x, self._game_configuration.window_height - random_pos, self._game_configuration.pipe_width, random_pos, PipeDirection.Up)

        self._pipe_group.add(top_pipe)
        self._pipe_group.add(bottom_pipe)
        
    def __create_pipe_part__(self, x, y, width, height, pipe_direction):
        pipe_img = self._asset_factory.create_pipe_image((width, height), pipe_direction)
        return Pipe(x, y, pipe_img, self._game_configuration.map_move_speed)

    def __add_pipe_from_end__(self):
        last_pipe = self._pipe_group.sprites()[-1]
        new_pipe_x = last_pipe.rect.x + self._game_configuration.pipe_width + self._game_configuration.pipe_distance
        self.__create_pipe__(new_pipe_x)

    def update(self):
        # Add more pipes if there's space
        # Each pipe actually has two parts, top and bottom
        num_sprites_to_add = self._max_num_pipes - len(self._pipe_group.sprites())
        if (num_sprites_to_add > 0):
            for i in range(num_sprites_to_add):
                self.__add_pipe_from_end__()