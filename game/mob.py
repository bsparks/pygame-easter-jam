import pygame
import random
from pygame.math import Vector2
from pygame.sprite import Sprite
from engine.event_handler import EventHandler
from engine.assets import load_image
from .floating_text import FloatingText


class Mob(EventHandler, Sprite):
    def __init__(self, game, name, image_name, collision_rect=None):
        Sprite.__init__(self)
        EventHandler.__init__(self)
        self.game = game
        self.name = name
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
        self.xp = 1
        self.damage = 1
        self.target = None
        
    def take_damage(self, amount):
        # only show decimal if it's not 0
        render_amount = int(amount) if amount.is_integer() else amount
        dmg_text = FloatingText(render_amount, self.rect.center)
        self.game.state.damage_texts.add(dmg_text)
        self.health -= amount
        if self.health <= 0:
            self.die()
            
    def die(self):
        self.emit("die", self)
        self.kill()
        
    def update(self, dt):
        screen_rect = self.game.screen.get_rect()

        # keep collision rect centered on sprite rect
        self.collision_rect.center = self.rect.center

        move_dir = Vector2(0, 0)
        if self.target is not None:
            move_dir = Vector2(self.target.rect.center) - Vector2(self.rect.center)
            if move_dir.magnitude() != 0:
                move_dir.normalize_ip()
                
        # if I am outside the screen, then dont worry about collision
        if not screen_rect.contains(self.collision_rect):
            self.rect.center += move_dir * self.move_speed / 100 * dt
            return
                
        # check if future location based on move_dir is colliding with anyone else in the group
        future_rect = self.collision_rect.copy()
        future_rect.center += move_dir * self.move_speed / 100 * dt
        main_group = self.groups()[0]
        for sprite in main_group:
            if sprite is not self and future_rect.colliderect(sprite.collision_rect):
                # wiggle in a random direction
                move_dir = Vector2(random.uniform(-5, 5), random.uniform(-5, 5))
                # stop
                # move_dir = Vector2(0, 0)
                break
        
        self.rect.center += move_dir * self.move_speed / 100 * dt