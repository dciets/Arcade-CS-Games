import os
import random
import pygame
from pygame.locals import *
from input_map import *
from minigames import multiplayer
from minigames.mirrors.entities.mirror import Mirror


class MirrorsMinigame(multiplayer.Minigame):
    name = "Break The Mirrors!"

    MIRROR_BASE_COUNT = 2
    MIRROR_BASE_SPEED = 10
    MIRROR_BASE_COOLDOWN = 100

    def init(self):
        self.mirrors = []
        self.mirror_count = MirrorsMinigame.MIRROR_BASE_COUNT
        self.mirror_speed = MirrorsMinigame.MIRROR_BASE_SPEED
        self.mirror_cooldown = 0
        self.results = [False, False]

    def tick(self):
        if self.mirror_cooldown == 0:
            self.mirror_cooldown = MirrorsMinigame.MIRROR_BASE_COOLDOWN

            self.mirrors.append(Mirror(self.screen))
        else:
            self.mirror_cooldown -= 1

        for m in self.mirrors:
            m.animate()

    def get_results(self):
        return self.results
