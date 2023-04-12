import pygame
from pygame.math import Vector2
from pygame.sprite import Sprite
from engine.event_handler import EventHandler
from engine.assets import load_image


class Mob(EventHandler, Sprite):
    def __init__(self, image_name):
        Sprite.__init__(self)
        EventHandler.__init__(self)
        self.image = load_image(image_name)
        self.rect = pygame.rect.FRect(self.image.get_rect())
        self.rect.centerx -= self.rect.width / 2
        self.rect.centery -= self.rect.height / 2
        
        self.move_speed = 5
        self.health = 5
        self.target = None
        
    def update(self, dt):
        if self.target is not None:
            move_dir = Vector2(self.target.rect.center) - Vector2(self.rect.center)
            if move_dir.magnitude() != 0:
                move_dir.normalize_ip()
            self.rect.center += move_dir * self.move_speed / 100 * dt