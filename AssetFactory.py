import os

from pygame import image, transform, Rect, Surface

from typing import Tuple

dirname = os.path.dirname(__file__)
pipe_img_path = os.path.join(dirname, r"assets\pipe.png")
flappy_bird_img_path = os.path.join(dirname, r"assets\flappy-bird.png")


class PipeOrientation:
    """ The pipe orientation """
    Up = 0
    Down = 1


class AssetFactory:
    """ A factory class to create pygame images """
    def __init__(self):
        self._pipe_up_img_base = image.load(pipe_img_path)
        self._flappy_bird_img_base = image.load(flappy_bird_img_path)

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
