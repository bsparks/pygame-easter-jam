from pygame.math import Vector2
from pygame.sprite import Sprite
from engine.event_handler import EventHandler
from engine.assets import load_image


class Pickup(Sprite, EventHandler):
    def __init__(self, image_name):
        Sprite.__init__(self)
        EventHandler.__init__(self)
        self.image = load_image(image_name)
        self.rect = self.image.get_rect()
        self.position = Vector2(0, 0)

    def on_collsiion(self, other):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.blit(self.image, self.position + self.rect.center)
