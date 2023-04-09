from engine.state import State
import pygame
from engine.colors import *
from engine.assets import load_music, load_font, load_image
from engine.particles import ParticleEmitter

class MainMenu(State):
    def __init__(self, game):
        super().__init__(game)
        self.screen = game.screen
        
    def enter(self):
        load_music("Merged.mid")
        pygame.mixer.music.play(-1)
        title_font = load_font("PressStart2P-Regular.ttf", 50)
        self.title = "EASTER"
        self.subtitle = "SURVIVORS"
        subtitle_font = load_font("PressStart2P-Regular.ttf", 32)
        self.subtitle_text = subtitle_font.render(self.subtitle, True, "white")
        self.title_texts = []
        self.emitters = []
        for i in range(len(self.title)):
            self.title_texts.append(title_font.render(self.title[i], True, "#9b4d53"))
            
        for i in range(len(self.title)):
            self.emitters.append(ParticleEmitter(pygame.math.Vector2(150 + i * 150, 150), 100, (1, 10), (-1.0, 1.0), (0.1, 1.0), [PURPLE, GREEN, BLUE, ORANGE, YELLOW, PINK], 600))
        
        self.big_bunny = load_image("bunny_vamp.png")
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.game.change_state("play")
        
    def update(self, dt):
        # print(f"frame time: {dt}ms")
        for emitter in self.emitters:
            emitter.update(dt)
        #self.emitter.update(dt)
    
    def draw(self):
        self.screen.fill("#3E4772")

        self.screen.blit(self.big_bunny, (512, 128+64))
        
        pygame.draw.ellipse(self.screen, PURPLE, (100, 100, 100, 100))
        pygame.draw.ellipse(self.screen, PINK, (250, 100, 100, 100))
        pygame.draw.ellipse(self.screen, YELLOW, (400, 100, 100, 100))
        pygame.draw.ellipse(self.screen, GREEN, (550, 100, 100, 100))
        pygame.draw.ellipse(self.screen, BLUE, (700, 100, 100, 100))
        pygame.draw.ellipse(self.screen, ORANGE, (850, 100, 100, 100))
        
        self.screen.blit(self.subtitle_text, (200, 350))
        
        for i in range(len(self.title_texts)):
            self.screen.blit(self.title_texts[i], (125 + i * 150, 125))
        for emitter in self.emitters:
            emitter.draw(self.screen)