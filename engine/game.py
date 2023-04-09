import pygame
from .colors import *
from .assets import load_music

class Game():
    def __init__(self, screen):
        self.state = "menu"
        self.screen = screen
        
    def startup(self):
        load_music("Merged.mid")
        pygame.mixer.music.play(-1)
        
    def update(self, dt):
        print(f"frame time: {dt}ms")
    
    def draw(self):
        pygame.draw.ellipse(self.screen, PURPLE, (100, 100, 100, 100))
        pygame.draw.ellipse(self.screen, PINK, (200, 100, 100, 100))
        pygame.draw.ellipse(self.screen, YELLOW, (300, 100, 100, 100))
        pygame.draw.ellipse(self.screen, GREEN, (400, 100, 100, 100))
        pygame.draw.ellipse(self.screen, BLUE, (500, 100, 100, 100))
        pygame.draw.ellipse(self.screen, ORANGE, (600, 100, 100, 100))