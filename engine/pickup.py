from pygame.math import Vector2
from pygame.sprite import Sprite
from engine.event_handler import EventHandler
from engine.assets import load_image


class Pickup(EventHandler, Sprite):
    def __init__(self, image_name):
        Sprite.__init__(self)
        EventHandler.__init__(self)
        self.image = load_image(image_name)
        self.rect = self.image.get_rect()
        self.rect.centerx -= self.rect.width // 2
        self.rect.centery -= self.rect.height // 2
        
    @property
    def position(self):
        return self.rect.center
    
    @position.setter
    def position(self, value):
        self.rect.center = value

    def on_pickup(self, other):
        print(f"Pickup {self} collided with {other}")

    def update(self, dt):
        pass
