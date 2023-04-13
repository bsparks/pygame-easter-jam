from engine.state import State
import pygame
import random
from pygame.sprite import Group
from engine.colors import *
from engine.assets import load_music, load_font, load_image
from engine.timer import Timer
from engine.pbar import ProgressBar
from .xp_pickup import XpPickup
from .player import Player
from .mob_factory import MobFactory
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

        self.player = Player(self.game)
        self.player.rect.center = self.game.screen.get_rect().center
        self.player.add_listener("level_up", self.handle_player_level_up)

        self.xp_bar = ProgressBar(pygame.math.Vector2(
            180, 10), (1000, 16), PURPLE, self.player.get_xp_needed())
        self.level_font = load_font("PressStart2P-Regular.ttf", 16)
        self.level_text = self.level_font.render(
            "Level: {}".format(self.player.level), True, "white")
        
        self.pickup_sound = pygame.mixer.Sound(buffer=pyfxr.pickup())
        self.pickup_sound.set_volume(0.1)
        
        self.damage_texts = Group()
        
        self.mobs = MobFactory(self.game)
        self.mobs.start()
        
        self.pickups = Group()
        for i in range(50):
            pickup = XpPickup(random.randint(1, 10))
            pickup.position = (random.randint(0, self.game.screen.get_width()), random.randint(0, self.game.screen.get_height()))
            self.pickups.add(pickup)

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
        self.pickups.update(dt)
        self.mobs.update(dt)
        self.damage_texts.update(dt)
        
        
        pickups = pygame.sprite.spritecollide(self.player, self.pickups, False)
        for pickup in pickups:
            self.pickup_sound.play()
            pickup.on_pickup(self.player)

    def draw(self):
        self.game.screen.fill(GREEN)

        self.player.draw(self.game.screen)
            
        self.pickups.draw(self.game.screen)
        self.mobs.draw(self.game.screen)
        self.damage_texts.draw(self.game.screen)

        self.level_timer.draw(self.game.screen)
        self.xp_bar.draw(self.game.screen)

        self.game.screen.blit(self.level_text, (10, 10))
