from engine.state import State
import pygame
import random
from pygame.sprite import Group
from engine.colors import *
from engine.assets import load_music, load_font, load_image
from engine.timer import Timer
from engine.pbar import ProgressBar
from .xp_pickup import XpPickup
from .player import Player, upgrade_types
from .mob_factory import MobFactory
from engine.particles import ParticleEmitter
import pyfxr


class PlayState(State):
    def enter(self):
        self.paused = False
        self.game_over = False
        self.choose_upgrades = False
        self.final_boss = False
        
        self.upgrade_selection = []
        self.upgrade_emitters = []
        
        for i in range(5):
            emitter = ParticleEmitter(pygame.math.Vector2(150 + i * 150, random.randint(10, 500)), random.randint(100, 200), (1, 10), (-1.0, 1.0), (0.1, 1.0), [PURPLE, GREEN, BLUE, ORANGE, YELLOW, PINK], 600)
            self.upgrade_emitters.append(emitter)
        
        game_over_font = load_font("PressStart2P-Regular.ttf", 64)
        self.game_over_lose_text = game_over_font.render("You Lose!", True, RED)
        self.game_over_win_text = game_over_font.render("You Win!", True, YELLOW)

        self.musics = ["merged2.mid", "merged3.mid", "merged4.mid", "merged5.mid"]
        self.current_music = None
        self.play_random_music()
        
        timer_font = load_font("PressStart2P-Regular.ttf", 32)
        five_minutes = 5 * 60 * 1000  # 5 minutes
        screen_width = self.game.screen.get_width()
        self.level_timer = Timer(
            five_minutes, (screen_width // 2, 48), timer_font)
        # TODO: wait for the level to finish loading and then start the timer
        self.level_timer.start()
        self.level_timer.add_listener(
            "complete", self.handle_level_timer_complete)
        self.level_timer.add_listener("second", self.handle_level_timer_second)
        self.level_timer.add_listener("minute", self.handle_level_timer_minute)

        self.player = Player(self.game)
        self.player.rect.center = self.game.screen.get_rect().center
        self.player.add_listener("level_up", self.handle_player_level_up)
        self.player.add_listener("die", self.handle_player_die)

        self.xp_bar = ProgressBar(pygame.math.Vector2(
            180, 10), (900, 16), PURPLE, self.player.get_xp_needed())
        self.level_font = load_font("PressStart2P-Regular.ttf", 16)
        self.level_text = self.level_font.render(
            "Level: {}".format(self.player.level), True, YELLOW)
        self.score = 0
        self.score_font = load_font("PressStart2P-Regular.ttf", 16)
        self.score_text = self.score_font.render("Score: {}".format(self.score), True, ORANGE)
        
        self.pickup_sound = pygame.mixer.Sound(buffer=pyfxr.pickup())
        self.pickup_sound.set_volume(0.1)
        
        self.mob_kill_sound = pygame.mixer.Sound(buffer=pyfxr.explosion())
        self.mob_kill_sound.set_volume(0.1)
        
        self.damage_texts = Group()
        
        self.mobs = MobFactory(self.game)
        self.mobs.add_listener("mob_die", self.handle_mob_die)
        self.mobs.start()
        
        self.pickups = Group()
        for i in range(20):
            pickup = XpPickup(1)
            pickup.position = (random.randint(0, self.game.screen.get_width()), random.randint(0, self.game.screen.get_height()))
            self.pickups.add(pickup)
            
    def play_random_music(self):
        music = random.choice(self.musics)
        while music == self.current_music:
            music = random.choice(self.musics)
        self.current_music = music
        load_music(music)
        pygame.mixer.music.play(-1)
            
    def increase_score(self, amount):
        self.score += amount
        self.score_text = self.score_font.render("Score: {}".format(self.score), True, ORANGE)
            
    def handle_mob_die(self, mob):
        self.mob_kill_sound.play()
        self.pickups.add(XpPickup(mob.xp, mob.rect.center))
        self.increase_score(mob.xp * 100)
        if self.final_boss and mob.name == "bunny_vamp_boss":
            self.final_boss = False
            self.game_over = True
            self.paused = True
        
    def handle_player_die(self):
        self.paused = True
        self.game_over = True

    def handle_player_level_up(self):
        self.xp_bar.max_value = self.player.get_xp_needed()
        self.level_text = self.level_font.render(
            "Level: {}".format(self.player.level), True, YELLOW)
        self.increase_score(500)
        self.setup_upgrades()
        
    def setup_upgrades(self):
        self.paused = True
        self.choose_upgrades = True
        # choose 3 of the upgrade_types keys
        self.upgrade_selection = random.sample(sorted(upgrade_types), 3)
        self.upgrade_texts = []
        name_font = load_font("PressStart2P-Regular.ttf", 16)
        desc_font = load_font("PressStart2P-Regular.ttf", 12)
        for upgrade in self.upgrade_selection:
            upgrade_data = upgrade_types[upgrade]
            name_text = name_font.render(upgrade_data["name"], True, YELLOW, None, 200)
            desc_text = desc_font.render(upgrade_data["description"], True, YELLOW, None, 200)
            self.upgrade_texts.append((name_text, desc_text))

    def handle_level_timer_complete(self):
        self.paused = True
        self.game_over = True
        
    def handle_level_timer_second(self, second):
        # print(f"Second! {second}")
        if second == 20:
            self.mobs.current_mob_types.append("egg_zombie")
            self.mobs.spawn_amount = 2
            
        if second == 60:
            # one time mass spawn
            for i in range(10):
                self.mobs.spawn_mob("egg_bat")
        
        if second == 80:
            self.mobs.current_mob_types.append("egg_skelington")
            self.mobs.spawn_amount = 3
            
        if second == 100:
            for i in range(20):
                self.mobs.spawn_mob()

        if second == 120:
            # spawn a mini boss
            self.mobs.spawn_mob("egg_big_mean")

        if second == 130:
            self.mobs.current_mob_types.append("egg_barbarian")
            self.mobs.spawn_amount = 5
            
        if second > 270 < 290:
            for i in range(10):
                self.mobs.spawn_mob()
                
        if second == 290:
            self.mobs.pause()
            self.mobs.group.empty()
            self.mobs.spawn_mob("bunny_vamp_boss")
            self.final_boss = True
        
    def handle_level_timer_minute(self, minute):
        # print(f"Minute! {minute}")
        self.play_random_music()
        self.increase_score(1000)
        if minute == 2: # technically the first minute has passed immediately
            self.mobs.current_mob_types.append("egg_werewolf")

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_over:
                        self.game.change_state("main_menu")
                    elif self.choose_upgrades:
                        self.player.apply_upgrade(random.choice(self.upgrade_selection))
                        self.choose_upgrades = False
                        self.paused = False
                    else:
                        self.paused = not self.paused
                elif event.key == pygame.K_1:
                    if self.choose_upgrades:
                        self.player.apply_upgrade(self.upgrade_selection[0])
                        self.choose_upgrades = False
                        self.paused = False
                elif event.key == pygame.K_2:
                    if self.choose_upgrades:
                        self.player.apply_upgrade(self.upgrade_selection[1])
                        self.choose_upgrades = False
                        self.paused = False
                elif event.key == pygame.K_3:
                    if self.choose_upgrades:
                        self.player.apply_upgrade(self.upgrade_selection[2])
                        self.choose_upgrades = False
                        self.paused = False

        if not self.paused:
            self.player.handle_events(events)

    def update(self, dt):
        if not self.paused:
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
        self.game.screen.blit(self.score_text, (1100, 10))
        
        if self.paused and self.game_over:
            self.draw_game_over()
        
        if self.paused and self.choose_upgrades:
            self.draw_upgrades()
        
    def draw_game_over(self):
        screen_width = self.game.screen.get_width()
        screen_height = self.game.screen.get_height()
        if self.game_over:
            if not self.player.alive:
                text_width, text_height = self.game_over_lose_text.get_size()
                self.game.screen.blit(self.game_over_lose_text, (screen_width // 2 - text_width // 2, screen_height // 2 - text_height // 2))
            else:
                text_width, text_height = self.game_over_win_text.get_size()
                self.game.screen.blit(self.game_over_win_text, (screen_width // 2 - text_width // 2, screen_height // 2 - text_height // 2))
                
    def draw_upgrades(self):
        screen_width, screen_height = self.game.screen.get_size()
        
        for emitter in self.upgrade_emitters:
            emitter.update(16)
            emitter.draw(self.game.screen)
        
        box_size = 256
        boxes = []
        # draw 3 rectangles evenly spaced across the screen for the background
        for i in range(3):
            box = pygame.Rect(128 + ((i * box_size) + ((i + 1) * 64)) , screen_height // 2 - box_size // 2, box_size, box_size)
            boxes.append(box)
        
        i = 0
        for box in boxes:
            pygame.draw.rect(self.game.screen, PURPLE, box)
            pygame.draw.rect(self.game.screen, "white", box, 8)
            self.game.screen.blit(self.upgrade_texts[i][0], (box.x + 16, box.y + 16))
            self.game.screen.blit(self.upgrade_texts[i][1], (box.x + 16, box.y + 192))
            i += 1
