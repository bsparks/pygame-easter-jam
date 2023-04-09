from engine.state import State
import pygame
from engine.colors import *
from engine.assets import load_music, load_font, load_image
from engine.timer import Timer

class PlayState(State):
    def enter(self):
        timer_font = load_font("PressStart2P-Regular.ttf", 32)
        five_minutes = 5 * 60 * 1000 # 5 minutes
        screen_width = self.game.screen.get_width()
        self.level_timer = Timer(five_minutes, (screen_width // 2, 32), timer_font)
        self.level_timer.start() # TODO: wait for the level to finish loading and then start the timer
        self.pimage = load_image("mr_bunny.png")
        self.bat = load_image("egg_bat_1.png")
        
    def update(self, dt):
        self.level_timer.update(dt)
        
    def draw(self):
        self.game.screen.fill(GREEN)
        
        self.level_timer.draw(self.game.screen)
        
        self.game.screen.blit(self.pimage, (100, 100))
        
        self.game.screen.blit(self.bat, (200, 200))