import pygame
from pygame.sprite import Sprite
from engine.assets import load_font

class FloatingText(Sprite):
    def __init__(self, value, start, size = 16, color = "white") -> None:
        Sprite.__init__(self)
        self.value = value
        self.size = size
        self.color = color
        self.font = load_font("PressStart2P-Regular.ttf", self.size)
        self.image = self.font.render(str(self.value), False, self.color)
        self.rect = pygame.rect.FRect(self.image.get_rect())
        self.rect.center = start
        self.speed = 0.1
        self.life = 1
        
    def update(self, dt):
        self.rect.centery -= self.speed * dt
        self.life -= dt / 1000
        # fade alpha
        self.image.set_alpha(self.life * 255)
        if self.life <= 0:
            self.kill()