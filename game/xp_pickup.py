import pygame
from .player import Player
from engine.pickup import Pickup

class XpPickup(Pickup):
    def __init__(self, value, position = None):
        image_name = "green_bean.png"
        if value >= 5 < 10:
            image_name = "blue_bean.png"
        elif value >= 10 < 15:
            image_name = "yellow_bean.png"
        elif value >= 15 < 20:
            image_name = "purple_bean.png"
        elif value >= 20:
            image_name = "red_bean.png"

        Pickup.__init__(self, image_name)
        self.value = value
        if position is not None:
            self.position = position
            
        self.target = None
        self.magnet_speed = 0.3
        
    def on_pickup(self, other):
        if isinstance(other, Player):
            other.add_xp(self.value)
        self.kill()
        
    def update(self, dt):
        if self.target is not None:
            #fly towards target
            direction = pygame.Vector2(self.target) - pygame.Vector2(self.rect.center)
            if direction.magnitude() != 0:
                direction.normalize_ip()
            self.rect.center += direction * self.magnet_speed * dt
            
        if len(self.groups()) == 0:
            return

        # if it touches other xp pickups, it will merge them
        my_group = self.groups()[0]
        for other in my_group:
            if other is not self:
                if self.rect.colliderect(other.rect):
                    XpPickup(self.value + other.value, self.position).add(my_group)
                    other.kill()
                    self.kill()
                    break