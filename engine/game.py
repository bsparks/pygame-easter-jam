import pygame
from .colors import *
from .assets import load_music, load_font
from .particles import ParticleEmitter

class Game():
    def __init__(self, screen):
        self.state = "menu"
        self.screen = screen
        
    def startup(self):
        load_music("Merged.mid")
        pygame.mixer.music.play(-1)
        title_font = load_font("PressStart2P-Regular.ttf", 32)
        self.title_text = title_font.render("EASTER", True, "white")
        
        self.emitter = ParticleEmitter(pygame.math.Vector2(150, 150), 100, (1, 10), (-1.0, 1.0), (0.1, 1.0), [PURPLE, GREEN, BLUE, ORANGE, YELLOW, PINK], 500)
        
        
    def update(self, dt):
        # print(f"frame time: {dt}ms")
        self.emitter.update(dt)
    
    def draw(self):
        pygame.draw.ellipse(self.screen, PURPLE, (100, 100, 100, 100))
        pygame.draw.ellipse(self.screen, PINK, (200, 100, 100, 100))
        pygame.draw.ellipse(self.screen, YELLOW, (300, 100, 100, 100))
        pygame.draw.ellipse(self.screen, GREEN, (400, 100, 100, 100))
        pygame.draw.ellipse(self.screen, BLUE, (500, 100, 100, 100))
        pygame.draw.ellipse(self.screen, ORANGE, (600, 100, 100, 100))
        self.screen.blit(self.title_text, (100, 300))
        self.emitter.draw(self.screen)