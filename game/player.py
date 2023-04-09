import pygame
from pygame.sprite import Sprite
from engine.assets import load_music, load_font, load_image

class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.input = pygame.math.Vector2(0, 0)
        self.position = pygame.math.Vector2(0, 0)
        self.image = load_image("mr_bunny.png")
        self.rect = self.image.get_rect()
        self.move_speed = 1
        
    def handle_events(self, events):
        self.input.x = 0
        self.input.y = 0
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.input.y = -1
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.input.y = 1
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.input.x = -1
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.input.x = 1

    def update(self, dt):
        self.position += self.input * self.move_speed * dt
    
    def draw(self, surface):
        surface.blit(self.image, self.position + self.rect.center)
        self.debug_draw(surface)
        
    def debug_draw(self, surface):
        pygame.draw.rect(surface, "red", (self.position[0] + self.rect.centerx, self.position[1] + self.rect.centery, self.rect.width, self.rect.height), 2)