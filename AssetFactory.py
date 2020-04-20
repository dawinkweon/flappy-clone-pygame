import os
from pygame import image, transform, Rect

dirname = os.path.dirname(__file__)
pipe_img_path = os.path.join(dirname, r"assets\pipe.png")
flappy_bird_img_path = os.path.join(dirname, r"assets\flappy-bird.png")

class PipeDirection:
    Up = 0
    Down = 1

class AssetFactory:
    def __init__(self):
        print(pipe_img_path)
        self.pipe_up_base = image.load(pipe_img_path)
        self.flappy_bird = image.load(flappy_bird_img_path)
        
    def create_pipe_image(self, width, height, pipe_direction):
        chopped_img = self.pipe_up_base.subsurface(Rect(0, 0, width, height))

        if pipe_direction == PipeDirection.Down:
            return transform.flip(chopped_img, False, True)
        return chopped_img

    def create_flappy_bird_image(self, width, height):
        return transform.scale(self.flappy_bird, (width, height))