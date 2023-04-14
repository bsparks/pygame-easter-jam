import random
import pygame
from pygame.sprite import Group
from engine.timer import Timer
from .mob import Mob
from engine.event_handler import EventHandler

mob_types = {
    "egg_bat": {
        "image_name": "egg_bat_1.png",
        "collision_rect": (1, 22, 61, 20),
        "health": 2,
        "speed": 5,
        "damage": 1,
        "xp": 1,
    },
    "egg_zombie": {
        "image_name": "egg_choc_zombie.png",
        "collision_rect": (16, 8, 33, 47),
        "health": 4,
        "speed": 3,
        "damage": 2,
        "xp": 2,
    },
    "egg_werewolf": {
        "image_name": "egg_werewolf.png",
        "collision_rect": (17, 5, 30, 54),
        "health": 6,
        "speed": 5,
        "damage": 5,
        "xp": 5,
    },
    "egg_barbarian": {
        "image_name": "egg_barb.png",
        "collision_rect": (13, 5, 38, 53),
        "health": 10,
        "speed": 3,
        "damage": 10,
        "xp": 10,
    },
    "egg_big_mean": {
        "image_name": "egg_big_mean.png",
        "collision_rect": (26, 15, 76, 99),
        "health": 50,
        "speed": 2,
        "damage": 20,
        "xp": 30,
    },
}

class MobFactory(EventHandler):
    def __init__(self, game):
        EventHandler.__init__(self)
        self.game = game
        self.spawn_time = 5000
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
        
    def handle_mob_die(self, mob):
        self.emit("mob_die", mob)
            
    def spawn_mob(self, type_to_spawn = None):
        mob_type = random.choice(self.current_mob_types) if type_to_spawn is None else type_to_spawn
        mob_data = mob_types[mob_type]
        mob = Mob(self.game, mob_data["image_name"], mob_data["collision_rect"])
        mob.health = mob_data["health"]
        mob.move_speed = mob_data["speed"]
        mob.damage = mob_data["damage"]
        mob.xp = mob_data["xp"]
        mob.target = self.game.state.player
        mob.add_listener("die", self.handle_mob_die)
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
        #for mob in self.group:
            #pygame.draw.rect(self.game.screen, "red", mob.collision_rect, 1)