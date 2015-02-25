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
    MIRROR_BASE_COOLDOWN = 200

    def init(self):
        self._first_tick = True

        self.base = BlasterBase(2)
        self.mirrors = []
        self.mirror_count = MirrorsMinigame.MIRROR_BASE_COUNT
        self.mirror_speed = MirrorsMinigame.MIRROR_BASE_SPEED
        self.mirror_cooldown = 0
        self.score = [0, 0]
        self.results = [True, True]

    def tick(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                for i in range(len(self.base.blasters)):
                    if event.key == PLAYERS_MAPPING[i][UP]:
                        self.base.blasters[i].set_motion(Blaster.ACCELERATING)
                        self.base.blasters[i].set_direction(Blaster.RIGHT)
                    elif event.key == PLAYERS_MAPPING[i][DOWN]:
                        self.base.blasters[i].set_motion(Blaster.ACCELERATING)
                        self.base.blasters[i].set_direction(Blaster.LEFT)
                    elif event.key == PLAYERS_MAPPING[i][ACTION]:
                        self.base.blasters[i].set_action(Blaster.CHARGING)
            elif event.type == KEYUP:
                for i in range(len(self.base.blasters)):
                    if event.key == PLAYERS_MAPPING[i][UP]:
                        self.base.blasters[i].set_motion(Blaster.DECELERATING)
                        self.base.blasters[i].set_direction(Blaster.RIGHT)
                    elif event.key == PLAYERS_MAPPING[i][DOWN]:
                        self.base.blasters[i].set_motion(Blaster.DECELERATING)
                        self.base.blasters[i].set_direction(Blaster.LEFT)
                    elif event.key == PLAYERS_MAPPING[i][ACTION]:
                        self.base.blasters[i].set_action(Blaster.SHOOTING)

        if self.mirror_cooldown == 0 and len(self.mirrors) < MirrorsMinigame.MIRROR_BASE_COUNT:
            self.mirror_cooldown = MirrorsMinigame.MIRROR_BASE_COOLDOWN

            self.mirrors.append(Mirror((self.screen.get_width(), self.screen.get_height()), self.mirrors))
        else:
            self.mirror_cooldown -= 1

        self.base.display(self.screen)

        for m in self.mirrors:
            p = m.display(self.screen, 3, 150, 1000, self.base.get_bullets())

            if p is not None:
                m.destroy()
                del m
                self.score[p] += 1
                self.results[0] = self.score[0] >= self.score[1]
                self.results[1] = self.score[1] >= self.score[0]

    def get_results(self):
        return self.results
