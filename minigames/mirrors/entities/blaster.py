from math import sin, radians, cos
from itertools import cycle
import random
import pygame


class Blaster:
    SCALE = 3
    MAX_SPEED = 2
    ACCELERATION = 0.005
    DECELERATION = -0.005

    STOPPED = 0
    STOPPING = 1
    MOVING = 2

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

        self._t0 = -1
        self._v0 = 0
        self._v = 0
        self._status = Blaster.STOPPED
        self._angle = 0
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
        self._v0 = self._v

    def set_status(self, status):
        if self._status != status:
            self._v0 = self._v
            self._t0 = pygame.time.get_ticks()

        self._status = status

    def display(self, screen):
        if self._status == Blaster.MOVING:
            if self._direction == -1:
                self._v = max(self._v0 - Blaster.ACCELERATION * ((pygame.time.get_ticks() - self._t0)), -Blaster.MAX_SPEED)
                print "RIGHT"
                print self._v
            elif self._direction == 1:
                self._v = min(self._v0 + Blaster.ACCELERATION * ((pygame.time.get_ticks() - self._t0)), Blaster.MAX_SPEED)
                print "LEFT"
                print self._v
        elif self._status == Blaster.STOPPING and self._t0 != -1:
            if self._direction == -1:
                self._v = min(self._v0 - Blaster.DECELERATION * ((pygame.time.get_ticks() - self._t0)), 0)
            elif self._direction == 1:
                self._v = max(self._v0 + Blaster.DECELERATION * ((pygame.time.get_ticks() - self._t0)), 0)

            if self._v == 0:
                self._status = Blaster.STOPPED

        #print self._v
        self._angle += self._v

        sx = screen.get_width() / 2
        sy = screen.get_height() / 2
        dy = sin(radians(self._angle)) * Blaster.RADIUS
        dx = cos(radians(self._angle)) * Blaster.RADIUS

        rotated_gfx = pygame.transform.rotate(self.blaster_gfx[self.frame], 270 - self._angle)
        rect = rotated_gfx.get_rect(center=(sx + dx, sy + dy))

        screen.blit(rotated_gfx, rect)