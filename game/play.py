from engine.state import State
import pygame
import random
from engine.colors import *
from engine.assets import load_music, load_font, load_image
from engine.timer import Timer
from .player import Player

class PlayState(State):
    def enter(self):
        timer_font = load_font("PressStart2P-Regular.ttf", 32)
        five_minutes = 5 * 60 * 1000 # 5 minutes
        screen_width = self.game.screen.get_width()
        self.level_timer = Timer(five_minutes, (screen_width // 2, 32), timer_font)
        self.level_timer.start() # TODO: wait for the level to finish loading and then start the timer
        self.player = Player()
        self.bat = load_image("egg_bat_1.png")
        self.bats = [(random.randint(0, self.game.screen.get_width()), random.randint(0, self.game.screen.get_height())) for i in range(100)]
        
    def handle_events(self, events):
        self.player.handle_events(events)
        
    def update(self, dt):
        self.level_timer.update(dt)
        self.player.update(dt)
        
    def draw(self):
        self.game.screen.fill(GREEN)
        
        self.player.draw(self.game.screen)
        
        # draw 100 random bats on the screen
        for p in self.bats:
            self.game.screen.blit(self.bat, p)
            
        
        self.level_timer.draw(self.game.screen)