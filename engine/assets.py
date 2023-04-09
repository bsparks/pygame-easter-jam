import os
import pygame

def load_music(name):
    path = os.path.join("assets", "music", name)
    pygame.mixer.music.load(path)
