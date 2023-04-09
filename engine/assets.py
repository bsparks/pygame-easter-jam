import os
import pygame
from functools import cache

def load_music(name):
    path = os.path.join("assets", "music", name)
    pygame.mixer.music.load(path)

@cache
def load_font(name, size):
    path = os.path.join("assets", "fonts", name)
    return pygame.font.Font(path, size)