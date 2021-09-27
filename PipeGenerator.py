import random

from pygame.rect import Rect
from pygame.sprite import Group

from GameSettings import GameSettings
from AssetFactory import AssetFactory, PipeOrientation
from Pipe import Pipe
from PipeGap import PipeGap


class PipeGenerator:
    """ Class that generates pipes """

    # Each pipe has a top and bottom part
    NUM_PIPE_PARTS = 2

    def __init__(self, pipe_group: Group, pipe_gaps: Group, asset_factory: AssetFactory, game_settings: GameSettings):
        """ Constructor for the pipe generator

        @param pipe_group: the pipes group to generate pipes for
        @param pipe_gaps: the pipe gaps group to generate gaps for
        @param asset_factory: the asset factory
        @param game_settings: the game settings
        """
        self._asset_factory = asset_factory
        self._settings = game_settings
        self._pipe_group = pipe_group
        self._pipe_gaps = pipe_gaps

        self.can_move = True

        self._min_pipe_height = int(self._settings.window_height * 0.1)

    def create_pipe(self, pipe_x: int) -> None:
        allowed_range = self._settings.window_height \
                        - self._min_pipe_height \
                        - self._settings.pipe_gap_height
        random_pos = random.randint(self._min_pipe_height, allowed_range)
        top_height = self._settings.window_height - (random_pos + self._settings.pipe_gap_height)
        top_pipe = self.__create_pipe_part__(pipe_x, 0, self._settings.pipe_width, top_height,
                                             PipeOrientation.Down)
        bottom_pipe = self.__create_pipe_part__(pipe_x, self._settings.window_height - random_pos,
                                                self._settings.pipe_width, random_pos, PipeOrientation.Up)
        pipe_gap_rect = Rect(pipe_x, top_pipe.rect.bottom,
                             self._settings.pipe_width, self._settings.pipe_gap_height)
        pipe_gap = PipeGap(pipe_gap_rect)

        self._pipe_group.add(top_pipe)
        self._pipe_group.add(bottom_pipe)
        self._pipe_gaps.add(pipe_gap)

    def __create_pipe_part__(self, x: int, y: int, width: int, height: int, pipe_direction: PipeOrientation) -> Pipe:
        pipe_img = self._asset_factory.create_pipe_image((width, height), pipe_direction)
        return Pipe(x, y, pipe_img)

    def __add_pipe_from_end__(self) -> None:
        last_pipe = self._pipe_group.sprites()[-1]
        new_pipe_x = last_pipe.rect.x + self._settings.pipe_width + self._settings.pipe_distance
        self.create_pipe(new_pipe_x)