import os

from pygame import image, transform, Rect, Surface

from typing import Tuple

dirname = os.path.dirname(__file__)
pipe_img_path = os.path.join(dirname, "assets", "pipe.png")
flappy_bird_img_path = os.path.join(dirname, "assets", "flappy-bird.png")
bg_path = os.path.join(dirname, "assets", "bg.png")


class PipeOrientation:
    """ The pipe orientation """
    Up = 0
    Down = 1


class AssetFactory:
    """ A factory class to create pygame images """
    def __init__(self):
        print(pipe_img_path)
        self._pipe_up_img_base = image.load(pipe_img_path)
        self._flappy_bird_img_base = image.load(flappy_bird_img_path)
        self._bg_img = image.load(bg_path)

    def create_pipe_image(self, size: Tuple[int, int], orientation: PipeOrientation) -> Surface:
        """ Returns a pipe image

        @param size: the size of the pipe
        @param orientation: the orientation of the pipe
        @return: Returns a pipe image
        """
        pipe_img = self._pipe_up_img_base.subsurface(Rect(0, 0, size[0], size[1]))

        if orientation == PipeOrientation.Down:
            pipe_img = transform.flip(pipe_img, False, True)

        return pipe_img

    def create_flappy_bird_image(self, size: Tuple[int, int]) -> Surface:
        """ Returns a flappy bird image

        @param size: the size of the bird
        @return: the flappy bird image
        """
        return transform.scale(self._flappy_bird_img_base, size)

    def create_bg(self, width: int, height: int) -> Surface:
        """ Returns the game background

        @param size: the size of the background
        @return: the background image
        """
        return self._bg_img