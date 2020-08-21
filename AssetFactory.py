import os
from pygame import image, transform, Rect
from typing import Tuple

dirname = os.path.dirname(__file__)
pipe_img_path = os.path.join(dirname, r"assets\pipe.png")
flappy_bird_img_path = os.path.join(dirname, r"assets\flappy-bird.png")


class PipeDirection:
    Up = 0
    Down = 1


class AssetFactory:
    def __init__(self):
        self._pipe_up_img_base = image.load(pipe_img_path)
        self._flappy_bird_img_base = image.load(flappy_bird_img_path)

    def create_pipe_image(self, size: Tuple[int, int], pipe_direction: PipeDirection):
        pipe_img = self._pipe_up_img_base.subsurface(Rect(0, 0, size[0], size[1]))

        if pipe_direction == PipeDirection.Down:
            pipe_img = transform.flip(pipe_img, False, True)

        return pipe_img

    def create_flappy_bird_image(self, size: Tuple[int, int]):
        return transform.scale(self._flappy_bird_img_base, size)
