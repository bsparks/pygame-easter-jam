import random
import pygame
from pygame.sprite import Group
from engine.timer import Timer
from .mob import Mob

mob_types = {
    "egg_bat": {
        "image_name": "egg_bat_1.png",
        "collision_rect": (1, 22, 61, 20),
        "health": 5,
        "speed": 5,
        "damage": 1,
        "xp": 1,
    }
}

class MobFactory:
    def __init__(self, game):
        self.game = game
        self.spawn_time = 3000
        self.spawn_timer = Timer(self.spawn_time)
        self.spawn_timer.add_listener("complete", self.handle_spawn_timer_complete)
        self.spawn_amount = 1
        self.group = Group()
        self.current_mob_types = ["egg_bat"]
        
    def start(self):
        self.spawn_mob()
        self.spawn_timer.start()
        
    def pause(self):
        self.spawn_timer.pause()
        
    def handle_spawn_timer_complete(self):
        for i in range(self.spawn_amount):
            self.spawn_mob()
        self.spawn_timer.reset()
            
    def spawn_mob(self):
        mob_type = random.choice(self.current_mob_types)
        mob_data = mob_types[mob_type]
        mob = Mob(mob_data["image_name"], mob_data["collision_rect"])
        mob.health = mob_data["health"]
        mob.move_speed = mob_data["speed"]
        mob.damage = mob_data["damage"]
        mob.xp = mob_data["xp"]
        mob.target = self.game.state.player
        screen_width = self.game.screen.get_width()
        screen_height = self.game.screen.get_height()
        # spawn somewhere outside the screen, near the edge
        side = random.choice(["top", "bottom", "left", "right"])
        match side:
            case "top":
                spawn_point = (random.randint(0, screen_width), -mob.rect.height)
            case "bottom":
                spawn_point = (random.randint(0, screen_width), screen_height + mob.rect.height)
            case "left":
                spawn_point = (-mob.rect.width, random.randint(0, screen_height))
            case "right":
                spawn_point = (screen_width + mob.rect.width, random.randint(0, screen_height))
            
        mob.rect.center = spawn_point
        self.group.add(mob)
            
    def update(self, dt):
        self.spawn_timer.update(dt)
        self.group.update(dt)
        
    def draw(self, surface):
        self.group.draw(surface)
        # temp debug draw collsion rect
        for mob in self.group:
            pygame.draw.rect(self.game.screen, "red", mob.collision_rect, 1)