import pygame
from pygame.math import Vector2
from pygame.sprite import Sprite
from engine.event_handler import EventHandler
from engine.assets import load_image


class Mob(EventHandler, Sprite):
    def __init__(self, image_name, collision_rect=None):
        Sprite.__init__(self)
        EventHandler.__init__(self)
        self.image = load_image(image_name)
        self.rect = pygame.rect.FRect(self.image.get_rect())
        self.rect.centerx -= self.rect.width / 2
        self.rect.centery -= self.rect.height / 2
        
        if collision_rect is None:
            self.collision_rect = self.rect
        else:
            self.collision_rect = pygame.rect.FRect(collision_rect)
        
        self.move_speed = 5
        self.health = 5
        self.target = None
        
    def update(self, dt):
        # keep collision rect centered on sprite rect
        self.collision_rect.center = self.rect.center

        move_dir = Vector2(0, 0)
        if self.target is not None:
            move_dir = Vector2(self.target.rect.center) - Vector2(self.rect.center)
            if move_dir.magnitude() != 0:
                move_dir.normalize_ip()
                
        # check if future location based on move_dir is colliding with anyone else in the group
        future_rect = self.collision_rect.copy()
        future_rect.center += move_dir * self.move_speed / 100 * dt
        main_group = self.groups()[0]
        for sprite in main_group:
            if sprite is not self and future_rect.colliderect(sprite.collision_rect):
                # attempt to push slightly in the opposite direction
                # move_dir *= -1
                # stop
                move_dir = Vector2(0, 0)
                break
        
        self.rect.center += move_dir * self.move_speed / 100 * dt