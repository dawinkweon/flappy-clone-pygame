import random
from Pipe import Pipe

class PipeContainer:
    # Each pipe has a top and bottom part
    NUM_PIPE_PARTS = 2 
    def __init__(self, max_width, max_height, pipe_width, pipe_distance, pipe_gap_height):
        self.max_width = max_width
        self.max_height = max_height
        self.pipe_width = pipe_width
        self.pipe_distance = pipe_distance
        self.pipe_gap_height = pipe_gap_height
        self.min_pipe_height = int(max_height * 0.1)
        self.max_num_pipes = int(self.max_width / (self.pipe_width + self.pipe_distance)) * PipeContainer.NUM_PIPE_PARTS + 2 # Add 2 for some leeway
        self.pipes = []

    def initialize_pipes(self, pipe_start_pos_x):
        first_pipe_index = int(pipe_start_pos_x / (self.pipe_width + self.pipe_distance))

        for i in range(first_pipe_index, self.max_num_pipes):
            pipe_x = i * (self.pipe_width + self.pipe_distance)
            self.create_pipe(pipe_x)

    def create_pipe(self, pipe_x):
        random_pos = random.randint(self.min_pipe_height, self.max_height - self.min_pipe_height - self.pipe_gap_height)
        top_height = self.max_height - (random_pos + self.pipe_gap_height)
        top_pipe = Pipe(pipe_x, 0, self.pipe_width, top_height) 
        bottom_pipe = Pipe(pipe_x, self.max_height - random_pos, self.pipe_width, random_pos)
        
        self.pipes.append(top_pipe)
        self.pipes.append(bottom_pipe)

    def add_pipe_from_end(self):
        last_pipe = self.pipes[len(self.pipes) - 1]
        new_pipe_x = last_pipe.x + self.pipe_width + self.pipe_distance
        self.create_pipe(new_pipe_x)

    def tick(self):
        for pipe in self.pipes:
            pipe.move_left()
            if pipe.x <= 0:
                self.pipes.remove(pipe)

        # Add more pipes if there's space
        # Each pipe actually has two parts, top and bottom
        while(len(self.pipes) < self.max_num_pipes):
            self.add_pipe_from_end()

    def draw(self, pygame, game_display):    
        for pipe in self.pipes:
            pygame.draw.rect(game_display, Pipe.DrawColor, pygame.Rect(pipe.x, pipe.y, pipe.width, pipe.height))