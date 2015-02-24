from math import sin, radians, cos
from itertools import cycle
import random
import pygame


class Blaster:
    SCALE = 3
    ACCELERATION = 0
    STOP = 0
    START = 1
    LEFT = -1
    RIGHT = 1
    RADIUS = 70
    BLASTER_SPRITES = [ ["minigames/mirrors/images/blaster1_1.png",
                         "minigames/mirrors/images/blaster1_2.png",
                         "minigames/mirrors/images/blaster1_3.png"],
                        ["minigames/mirrors/images/blaster2_1.png",
                         "minigames/mirrors/images/blaster2_2.png",
                         "minigames/mirrors/images/blaster2_3.png"] ]
    LOS_SPRITES = [ ["minigames/mirrors/images/los1_1.png",
                     "minigames/mirrors/images/los1_2.png"],
                    ["minigames/mirrors/images/los2_1.png",
                     "minigames/mirrors/images/los2_2.png"] ]

    def __init__(self, player):
        self.blaster_gfx = []
        self.los_gfx = []
        self.frame = 0
        self.shooting = False

        self._v0 = 0
        self._theta0 = random.randint(0, 359)
        self._t0 = -1
        self._v = 0
        self._theta = 0
        self._status = Blaster.STOP
        self._direction = Blaster.RIGHT

        for path in Blaster.BLASTER_SPRITES[player]:
            img = pygame.image.load(path)
            img = pygame.transform.scale(img, (img.get_width() * Blaster.SCALE, img.get_height() * Blaster.SCALE))
            self.blaster_gfx.append(img)

        for path in Blaster.LOS_SPRITES[player]:
            img = pygame.image.load(path)
            #img = pygame.transform.scale(img, (img.get_width() * Blaster.SCALE, img.get_height() * Blaster.SCALE))
            self.los_gfx.append(img)

        self.los_gfx = cycle(self.los_gfx)

    def set_direction(self, direction):
        self._direction = direction

    def set_status(self, status):
        # if status != self._status:
        #     if self._t0 == -1:
        #         self._v0 = 0
        #     else:
        #         self._v0 = self._theta / (pygame.time.get_ticks() - self._t0)
        #
        #     self._theta0 = self._theta
        #     self._theta = 0
        #     self._t0 = -1

        self._status = status

    def display(self, screen):
        # if self._status == Blaster.START:
        #     if self._t0 == -1:
        #         self._t0 = pygame.time.get_ticks()
        #         _t = 0
        #     else:
        #         _t = pygame.time.get_ticks() - self._t0
        #
        #     self._theta = self._theta0 + 0.1 * (self._v0 * _t + (Blaster.ACCELERATION * _t ** 2) / 2 * self._direction)
        # elif self._status == Blaster.STOP:
        #     if self._t0 == -1:
        #         self._t0 = pygame.time.get_ticks()
        #         _t = 0
        #     else:
        #         _t = pygame.time.get_ticks() - self._t0
        #
        #     self._theta = self._theta0 - 0.1 * (self._v0 * _t + (-Blaster.ACCELERATION * _t ** 2) / 2 * self._direction)
        #
        # print self._theta

        sx = screen.get_width() / 2
        sy = screen.get_height() / 2
        dy = sin(radians(self._theta)) * Blaster.RADIUS
        dx = cos(radians(self._theta)) * Blaster.RADIUS

        rotated_gfx = pygame.transform.rotate(self.blaster_gfx[self.frame], 270 - self._theta)
        rect = rotated_gfx.get_rect(center=(sx + dx, sy + dy))

        screen.blit(rotated_gfx, rect)