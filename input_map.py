import pygame
from pygame.locals import *

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
ACTION = 4

PLAYERS_MAPPING = [
    [K_w, K_d, K_s, K_a, K_SPACE], # UP, RIGHT,  DOWN, LEFT, ACTION
    [K_UP, K_RIGHT, K_DOWN, K_LEFT, K_0], # UP, RIGHT,  DOWN, LEFT, ACTION
]

# Real mapping
# PLAYERS_MAPPING = [
#    [K_d, K_w, K_e, K_a, K_s], # UP, RIGHT,  DOWN, LEFT, ACTION
#    [K_h, K_j, K_u, K_k, K_i], # UP, RIGHT,  DOWN, LEFT, ACTION
# ]


def get_player_keys(player):
    keys = pygame.key.get_pressed()
    return [keys[k] for k in PLAYERS_MAPPING[player]]
