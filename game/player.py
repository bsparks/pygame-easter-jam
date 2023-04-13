import pygame
import math
from pygame.math import Vector2
from pygame.sprite import Sprite
from engine.assets import load_music, load_font, load_image
from engine.event_handler import EventHandler
from engine.pbar import ProgressBar
from engine.timer import Timer
from .weapon import Weapon

upgrade_types = {
    "health": {
        "name": "Health",
        "description": "Increases max health by 10",
        "attribute": "max_health",
        "amount": 10,
        "apply_type": "add",
    },
    "health_regen": {
        "name": "Health Regen",
        "description": "Regenerates +1 health every second",
        "attribute": "health_regen",
        "amount": 1,
        "apply_type": "add",
    },
    "move_speed": {
        "name": "Move Speed",
        "description": "Increases move speed by 10%",
        "attribute": "move_speed",
        "amount": 1.1,
        "apply_type": "multiply",
    },
    "damage_modifier": {
        "name": "Damage Modifier",
        "description": "Increases damage by 10% to all weapons",
        "attribute": "damage_modifier",
        "amount": 0.1,
        "apply_type": "add",
    },
    "damage_base": {
        "name": "Damage Base",
        "description": "Increases base damage by 1",
        "attribute": "damage_base",
        "amount": 1,
        "apply_type": "add",
    },
}

class Player(Sprite, EventHandler):
    def __init__(self, game):
        Sprite.__init__(self)
        EventHandler.__init__(self)
        self.game = game
        self.health = 100
        self.max_health = 100
        self.health_regen = 0
        self.damage_modifier = 1
        self.damage_base = 1
        self.alive = True
        self.xp = 0
        self.level = 1
        self.input = pygame.math.Vector2(0, 0)
        self.image = load_image("mr_bunny.png")
        self.rect = pygame.rect.FRect(self.image.get_rect())
        # center rect
        self.rect.centerx -= self.rect.width // 2
        self.rect.centery -= self.rect.height // 2
        self.collision_rect = pygame.rect.FRect((22, 4, 21, 55))
        self.move_speed = 10
        self.weapons = [Weapon("carrot_dagger")]
        self.facing = pygame.math.Vector2(0, 0)
        self.health_bar = ProgressBar(pygame.math.Vector2(self.rect.topleft), (64, 4), "red", self.max_health, self.health)
        self.health_regen_timer = Timer(1000)
        self.health_regen_timer.add_listener("complete", self.on_health_regen_timer_complete)
        self.health_regen_timer.start()
        
    def on_health_regen_timer_complete(self):
        self.heal(self.health_regen)
        self.health_regen_timer.reset()
        
    def apply_upgrade(self, upgrade_type):
        upgrade_data = upgrade_types[upgrade_type]
        attribute = upgrade_data["attribute"]
        apply_type = upgrade_data["apply_type"]
        amount = upgrade_data["amount"]
        if apply_type == "add":
            setattr(self, attribute, getattr(self, attribute) + amount)
        elif apply_type == "multiply":
            setattr(self, attribute, getattr(self, attribute) * amount)

    def heal(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        self.alive = False
        self.emit("die")

    def add_xp(self, amount):
        self.xp += amount
        self.check_level_up()

    def get_xp_needed(self):
        xp_needed = 5
        if self.level == 1:
            xp_needed = 5
        elif self.level > 1 < 20:
            xp_needed = 5 + (self.level - 1) * 10
        elif self.level >= 20 < 40:
            xp_needed = 5 + (self.level - 1) * 15
        elif self.level >= 40:
            xp_needed = 5 + (self.level - 1) * 20
        return xp_needed

    def check_level_up(self):
        xp_needed = self.get_xp_needed()
        if self.xp >= xp_needed:
            self.xp -= xp_needed
            self.level_up()
            return True
        return False

    def level_up(self):
        self.level += 1
        self.emit("level_up")

    def handle_events(self, events):
        self.input.x = 0
        self.input.y = 0
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            self.input.y = -1
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            self.input.y = 1
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            self.input.x = -1
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.input.x = 1

    def update(self, dt):
        if not self.alive:
            return
        
        self.health_regen_timer.update(dt)

        if self.input.magnitude() != 0:
            self.facing.x = self.input.x
            self.facing.y = self.input.y
            self.input.normalize_ip()

        speed = self.move_speed / 100 * dt
        self.input *= speed
        self.rect.center += self.input
        # print(self.input)
        self.collision_rect.center = self.rect.center
        
        # for now just have the player check for collisions with mobs directly
        for mob in self.game.state.mobs.group:
            if self.collision_rect.colliderect(mob.collision_rect):
                self.take_damage(mob.damage)
        
        self.health_bar.position.x = self.rect.topleft[0]
        self.health_bar.position.y = self.rect.topleft[1]
        self.health_bar.max_value = self.max_health
        self.health_bar.value = self.health
        
        # because the health was modified during this call, we need to check if the player died
        if not self.alive:
            return
        
        # TODO: this is messy, find a better way
        for w in self.weapons:
            side = self.rect.midright
            fx, fy = self.facing
            if fx == 1 and fy == 0:
                side = self.rect.midright
            elif fx == -1 and fy == 0:
                side = self.rect.midleft
            elif fx == 0 and fy == 1:
                side = self.rect.midbottom
            elif fx == 0 and fy == -1:
                side = self.rect.midtop
            elif fx > 0 and fy > 0:
                side = self.rect.bottomright
            elif fx < 0 and fy > 0:
                side = self.rect.bottomleft
            elif fx > 0 and fy < 0:
                side = self.rect.topright
            elif fx < 0 and fy < 0:
                side = self.rect.topleft
                
            w.fire_point.x = side[0]
            w.fire_point.y = side[1]
            w.fire_direction = self.facing
            w.update(dt)
            for projectile in w:
                for mob in self.game.state.mobs.group:
                    if projectile.collision_rect.colliderect(mob.collision_rect):
                        mob.take_damage((projectile.damage + self.damage_base) * self.damage_modifier)
                        projectile.kill()
                        break

    def draw(self, surface):
        if not self.alive:
            return

        surface.blit(self.image, self.rect)
        self.health_bar.draw(surface)
        # self.debug_draw(surface)
        for w in self.weapons:
            w.draw(surface)

    def debug_draw(self, surface):
        pygame.draw.rect(surface, "red", self.collision_rect, 2)
