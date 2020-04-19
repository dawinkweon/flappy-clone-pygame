from Events import Events

class Drawable:
    def __init__(self, obs, pygame, game_display):
        self.pygame = pygame
        self.game_display = game_display

        # Register events
        obs.on(Events.Tick, self.tick)
        obs.on(Events.Draw, self.draw)

    def tick(self):
        pass

    def draw(self):
        pass