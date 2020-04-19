from Events import Events

class Drawable:
    def __init__(self, obs):
        # Register events
        self.obs = obs
        obs.on(Events.Tick, self.tick)
        obs.on(Events.Draw, self.draw)
        obs.on(Events.KeyDown, self.key_down)

    def tick(self):
        pass

    def draw(self, pygame, game_display):
        pass

    def key_down(self, key_code):
        pass