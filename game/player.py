import pygame
import math
from pygame.sprite import Sprite
from engine.assets import load_music, load_font, load_image
from engine.event_handler import EventHandler


class Player(Sprite, EventHandler):
    def __init__(self):
        Sprite.__init__(self)
        EventHandler.__init__(self)
        self.health = 100
        self.max_health = 100
        self.alive = True
        self.xp = 0
        self.level = 1
        self.input = pygame.math.Vector2(0, 0)
        self.position = pygame.math.Vector2(0, 0)
        self.image = load_image("mr_bunny.png")
        self.rect = self.image.get_rect()
        self.move_speed = 10

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
        # fix diagonal movement
        dx, dy = self.input.x, self.input.y
        if self.input.x != 0 and self.input.y != 0:
            dx = self.input.x * math.sqrt(2) / 2
            dy = self.input.y * math.sqrt(2) / 2
        self.input.x = dx
        self.input.y = dy
        movement = self.input * (self.move_speed / 100) * dt
        self.position += movement

    def draw(self, surface):
        surface.blit(self.image, self.position + self.rect.center)
        self.debug_draw(surface)

    def debug_draw(self, surface):
        pygame.draw.rect(surface, "red", (self.position[0] + self.rect.centerx,
                         self.position[1] + self.rect.centery, self.rect.width, self.rect.height), 2)
