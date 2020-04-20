import random
from Pipe import Pipe
from Drawable import Drawable
import pygame
from AssetFactory import AssetFactory, PipeDirection

class PipeContainer(Drawable):
    # Each pipe has a top and bottom part
    NUM_PIPE_PARTS = 2 
    def __init__(self, obs, asset_factory, max_width, max_height, pipe_width, pipe_distance, pipe_gap_height, map_move_speed):
        super().__init__(obs)
        self.obs = obs
        self.asset_factory = asset_factory
        self.max_width = max_width
        self.max_height = max_height
        self.pipe_width = pipe_width
        self.pipe_distance = pipe_distance
        self.pipe_gap_height = pipe_gap_height
        self.map_move_speed = map_move_speed
        self.min_pipe_height = int(max_height * 0.1)
        self.max_num_pipes = int(self.max_width / (self.pipe_width + self.pipe_distance)) * PipeContainer.NUM_PIPE_PARTS + 2 # Add 2 for some leeway
        self.pipes = []
        self.can_move = True

    def initialize_pipes(self, pipe_start_pos_x):
        first_pipe_index = int(pipe_start_pos_x / (self.pipe_width + self.pipe_distance))

        for i in range(first_pipe_index, self.max_num_pipes):
            pipe_x = i * (self.pipe_width + self.pipe_distance)
            self.create_pipe(pipe_x)

    def create_pipe(self, pipe_x):
        random_pos = random.randint(self.min_pipe_height, self.max_height - self.min_pipe_height - self.pipe_gap_height)
        top_height = self.max_height - (random_pos + self.pipe_gap_height)
        
        top_pipe = self.create_pipe_part(pipe_x, 0, self.pipe_width, top_height, PipeDirection.Down)
        bottom_pipe = self.create_pipe_part(pipe_x, self.max_height - random_pos, self.pipe_width, random_pos, PipeDirection.Up)

        self.pipes.append(top_pipe)
        self.pipes.append(bottom_pipe)
        
    def create_pipe_part(self, x, y, width, height, pipe_direction):
        pipe_img = self.asset_factory.create_pipe_image(width, height, pipe_direction)
        return Pipe(x, y, width, height, pipe_img)

    def add_pipe_from_end(self):
        last_pipe = self.pipes[len(self.pipes) - 1]
        new_pipe_x = last_pipe.x + self.pipe_width + self.pipe_distance
        self.create_pipe(new_pipe_x)

    def tick(self):
        if not self.can_move:
            return

        for pipe in self.pipes:
            pipe.move_left(self.map_move_speed)
            if pipe.x <= 0:
                self.pipes.remove(pipe)

        # Add more pipes if there's space
        # Each pipe actually has two parts, top and bottom
        while(len(self.pipes) < self.max_num_pipes):
            self.add_pipe_from_end()

    def draw(self, pygame, game_display):    
        for pipe in self.pipes:
            game_display.blit(pipe.img, (pipe.x, pipe.y))

    def game_over(self):
        self.can_move = False

    def error_handler(self, message):
        print("Pipe container recieved message: ")

    def get_pipes_as_rect_list(self):
        def to_rect(pipe):
            return pygame.Rect(pipe.x, pipe.y, pipe.width, pipe.height)
        rect_list = []
        for pipe in self.pipes:
            rect_list.append(to_rect(pipe))
        return rect_list