import pygame
import pyfxr
from pygame.math import Vector2
from pygame.sprite import Sprite, Group
from engine.timer import Timer
from engine.assets import load_image

weapon_types = {
    "carrot_dagger": {
        "image_name": "carrot_weapon.png",
        "collision_rect": (1, 14, 30, 6),
        "fire_rate": 1000,
        "damage": 1,
        "range": 50,
        "speed": 20,
        "rotate": True
    },
}

class Projectile(Sprite):
    def __init__(self, weapon, start, direction, target = None):
        Sprite.__init__(self, weapon)
        self.weapon = weapon
        self.start = start
        self.direction = direction
        self.image = load_image(self.weapon.image_name)
        self.og_image = self.image
        self.angle = 0
        self.rect = pygame.rect.FRect(self.image.get_rect())
        self.rect.center = self.start
        self.collision_rect = pygame.rect.FRect(self.weapon.collision_rect)
        self.collision_rect.center = self.rect.center
        self.damage = self.weapon.damage
        self.range = self.weapon.range
        self.rotate = self.weapon.rotate
        self.move_speed = self.weapon.speed
        self.distance_travelled = 0
        self.target = target
        
    def update(self, dt):
        self.collision_rect.center = self.rect.center
        
        # target does homing
        if self.target is not None:
            self.direction = Vector2(self.target.rect.center) - Vector2(self.rect.center)

        if self.direction.magnitude() != 0:
            self.direction.normalize_ip()
            
        if self.rotate:
            self.angle = self.direction.angle_to(Vector2(1, 0))
            self.image = pygame.transform.rotate(self.og_image, self.angle)
        
        self.rect.center += self.direction * self.move_speed / 100 * dt
        self.distance_travelled = (self.rect.center - self.start).magnitude()
        
        if self.distance_travelled >= self.range:
            self.kill()

class Weapon(Group):
    def __init__(self, weapon_type):
        Group.__init__(self)
        weapon_data = weapon_types[weapon_type]
        self.image_name = weapon_data["image_name"]
        self.range = weapon_data["range"]
        self.damage = weapon_data["damage"]
        self.rotate = weapon_data["rotate"]
        self.speed = weapon_data["speed"]
        self.collision_rect = weapon_data["collision_rect"]
        self.fire_rate = weapon_data["fire_rate"]
        self.fire_timer = Timer(self.fire_rate)
        self.fire_timer.add_listener("complete", self.handle_fire_timer_complete)
        self.fire_timer.start()
        self.fire_sound = pygame.mixer.Sound(buffer=pyfxr.laser())
        self.fire_point = Vector2(0, 0)
        self.fire_direction = Vector2(0, 0)
        
    def update(self, dt):
        self.fire_timer.update(dt)
        super().update(dt)
        
    def handle_fire_timer_complete(self):
        # spawn a projectile
        self.spawn_projectile()
        self.fire_timer.reset()
        
    def spawn_projectile(self):
        projectile = Projectile(self, self.fire_point, self.fire_direction)