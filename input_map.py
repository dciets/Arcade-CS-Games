import pygame
from pygame.locals import *

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
ACTION = 4

PLAYERS_MAPPING = [
    [K_w, K_d, K_s, K_a, K_SPACE], # UP, RIGHT,  DOWN, LEFT, ACTION
    [K_UP, K_RIGHT, K_DOWN, K_LEFT, K_KP0], # UP, RIGHT,  DOWN, LEFT, ACTION
]

def get_player_keys(player):
    keys = pygame.key.get_pressed()
    return [keys[k] for k in PLAYERS_MAPPING[player]]


