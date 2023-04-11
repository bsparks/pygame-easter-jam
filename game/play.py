from engine.state import State
import pygame
import random
from engine.colors import *
from engine.assets import load_music, load_font, load_image
from engine.timer import Timer
from engine.pbar import ProgressBar
from .player import Player
import pyfxr


class PlayState(State):
    def enter(self):
        load_music("merged2.mid")
        # pygame.mixer.music.play(-1)
        timer_font = load_font("PressStart2P-Regular.ttf", 32)
        five_minutes = 5 * 60 * 1000  # 5 minutes
        screen_width = self.game.screen.get_width()
        self.level_timer = Timer(
            five_minutes, (screen_width // 2, 48), timer_font)
        # TODO: wait for the level to finish loading and then start the timer
        self.level_timer.start()
        self.level_timer.add_listener(
            "complete", self.handle_level_timer_complete)

        self.player = Player()
        self.player.add_listener("level_up", self.handle_player_level_up)

        self.bat = load_image("egg_bat_1.png")
        self.bats = [(random.randint(0, self.game.screen.get_width()), random.randint(
            0, self.game.screen.get_height())) for i in range(100)]
        self.xp_bar = ProgressBar(pygame.math.Vector2(
            180, 10), (1000, 16), PURPLE, self.player.get_xp_needed())
        self.level_font = load_font("PressStart2P-Regular.ttf", 16)
        self.level_text = self.level_font.render(
            "Level: {}".format(self.player.level), True, "white")
        
        self.pickup_sound = pygame.mixer.Sound(buffer=pyfxr.pickup())
        self.pickup_sound.set_volume(0.1)
        
        self.xp_beans = [(random.randint(0, self.game.screen.get_width()), random.randint(
            0, self.game.screen.get_height())) for i in range(50)]
        self.xp_bean = load_image("green_bean.png")
        self.xp_bean5 = load_image("red_bean.png")

    def handle_player_level_up(self):
        self.xp_bar.max_value = self.player.get_xp_needed()
        self.level_text = self.level_font.render(
            "Level: {}".format(self.player.level), True, "white")

    def handle_level_timer_complete(self):
        print("Level complete!")
        self.game.change_state("main_menu")

    def handle_events(self, events):
        self.player.handle_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.change_state("main_menu")
                if event.key == pygame.K_1:
                    self.player.add_xp(1)
                    self.pickup_sound.play()
                if event.key == pygame.K_2:
                    self.player.add_xp(5)
                if event.key == pygame.K_3:
                    self.player.add_xp(10)
                if event.key == pygame.K_4:
                    self.player.add_xp(50)

    def update(self, dt):
        self.level_timer.update(dt)
        self.player.update(dt)
        self.xp_bar.value = self.player.xp

    def draw(self):
        self.game.screen.fill(GREEN)

        self.player.draw(self.game.screen)

        # draw 100 random bats on the screen
        for p in self.bats:
            self.game.screen.blit(self.bat, p)
            
        for b in self.xp_beans:
            self.game.screen.blit(random.choice((self.xp_bean, self.xp_bean5)), b)

        self.level_timer.draw(self.game.screen)
        self.xp_bar.draw(self.game.screen)

        self.game.screen.blit(self.level_text, (10, 10))
