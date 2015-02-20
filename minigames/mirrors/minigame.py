import os
import random
import pygame
from pygame.locals import *
from input_map import *
from minigames import multiplayer
from minigames.mirrors.entities.bubble import Bubble
from minigames.mirrors.entities.mirror import Mirror


class MirrorsMinigame(multiplayer.Minigame):
    name = "Break The Mirrors!"

    MIRROR_BASE_COUNT = 3
    MIRROR_BASE_SPEED = 10
    MIRROR_BASE_COOLDOWN = 50

    def init(self):
        self.bubble = Bubble()
        self.mirrors = []
        self.mirror_count = MirrorsMinigame.MIRROR_BASE_COUNT
        self.mirror_speed = MirrorsMinigame.MIRROR_BASE_SPEED
        self.mirror_cooldown = 0
        self.results = [False, False]

    def tick(self):
        self.bubble.animate(self.screen)

        if self.mirror_cooldown == 0 and len(self.mirrors) < MirrorsMinigame.MIRROR_BASE_COUNT:
            self.mirror_cooldown = MirrorsMinigame.MIRROR_BASE_COOLDOWN

            self.mirrors.append(Mirror((self.screen.get_width(), self.screen.get_height())))
        else:
            self.mirror_cooldown -= 1

        for m in self.mirrors:
            m.show(self.screen, 3, 150, 1000)

    def get_results(self):
        return self.results
