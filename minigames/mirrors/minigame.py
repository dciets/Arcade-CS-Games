import os
import random
import pygame
from pygame.locals import *
from input_map import *
from minigames import multiplayer
from minigames.mirrors.entities.blaster import Blaster
from minigames.mirrors.entities.blaster_base import BlasterBase
from minigames.mirrors.entities.mirror import Mirror


class MirrorsMinigame(multiplayer.Minigame):
    name = "Break The Mirrors!"

    MIRROR_BASE_COUNT = 3
    MIRROR_BASE_SPEED = 10
    MIRROR_BASE_COOLDOWN = 50

    def init(self):
        self.base = BlasterBase(1)
        self.mirrors = []
        self.mirror_count = MirrorsMinigame.MIRROR_BASE_COUNT
        self.mirror_speed = MirrorsMinigame.MIRROR_BASE_SPEED
        self.mirror_cooldown = 0
        self.results = [False, False]

    def tick(self):
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                for i in range(len(self.base.blasters)):
                    if event.key == PLAYERS_MAPPING[i][UP]:
                        self.base.blasters[i].set_status(Blaster.MOVING)
                        self.base.blasters[i].set_direction(Blaster.RIGHT)
                    elif event.key == PLAYERS_MAPPING[i][DOWN]:
                        self.base.blasters[i].set_status(Blaster.MOVING)
                        self.base.blasters[i].set_direction(Blaster.LEFT)
            elif event.type == KEYUP:
                for i in range(len(self.base.blasters)):
                    if event.key == PLAYERS_MAPPING[i][UP]:
                        self.base.blasters[i].set_status(Blaster.STOPPING)
                        self.base.blasters[i].set_direction(Blaster.RIGHT)
                    elif event.key == PLAYERS_MAPPING[i][DOWN]:
                        self.base.blasters[i].set_status(Blaster.STOPPING)
                        self.base.blasters[i].set_direction(Blaster.LEFT)

        if self.mirror_cooldown == 0 and len(self.mirrors) < MirrorsMinigame.MIRROR_BASE_COUNT:
            self.mirror_cooldown = MirrorsMinigame.MIRROR_BASE_COOLDOWN

            self.mirrors.append(Mirror((self.screen.get_width(), self.screen.get_height()), self.mirrors))
        else:
            self.mirror_cooldown -= 1

        self.base.display(self.screen)

        for m in self.mirrors:
            m.display(self.screen, 3, 150, 1000)

    def get_results(self):
        return self.results
