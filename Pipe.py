from pygame.sprite import Sprite
from pygame import Surface


class Pipe(Sprite):
    def __init__(self, x: int, y: int, image: Surface, move_speed: float):
        Sprite.__init__(self)
        self.move_speed = move_speed
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def set_move_speed(self, move_speed: float) -> None:
        self.move_speed = move_speed

    def update(self) -> None:
        self.rect.x -= self.move_speed

        if self.rect.x <= 0:
            self.kill()
