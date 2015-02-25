from math import sin, radians, cos
from itertools import cycle
import random
import pygame
from minigames.mirrors.entities.bullet import Bullet


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
                         "minigames/mirrors/images/blaster1_3.png",
                         "minigames/mirrors/images/blaster1_2.png"],
                        ["minigames/mirrors/images/blaster2_1.png",
                         "minigames/mirrors/images/blaster2_2.png",
                         "minigames/mirrors/images/blaster2_3.png",
                         "minigames/mirrors/images/blaster2_2.png"] ]
    LOS_SPRITES = [ ["minigames/mirrors/images/los1_1.png",
                     "minigames/mirrors/images/los1_2.png"],
                    ["minigames/mirrors/images/los2_1.png",
                     "minigames/mirrors/images/los2_2.png"] ]

    def __init__(self, player):
        self._frame = 0
        self._is_shooting = False
        self._t0 = -1
        self._v0 = 0
        self._v = 0
        self._status = Blaster.STOPPED
        self._angle = 0
        self._direction = Blaster.RIGHT

        self.bullets = []
        self.player = player

        blaster_sprites = []
        for path in Blaster.BLASTER_SPRITES[player]:
            img = pygame.image.load(path)
            img = pygame.transform.scale(img, (img.get_width() * Blaster.SCALE, img.get_height() * Blaster.SCALE))
            blaster_sprites.append(img)

        los_sprites = []
        for path in Blaster.LOS_SPRITES[player]:
            img = pygame.image.load(path)
            los_sprites.append(img)

        self._blaster = cycle(blaster_sprites)
        self._los = cycle(los_sprites)
        self.blaster_gfx = self._default_blaster_gfx = self._blaster.next()
        self.los_gfx = self._los.next()

    def set_direction(self, direction):
        self._direction = direction
        self._v0 = self._v

    def set_status(self, status):
        if self._status != status:
            self._v0 = self._v
            self._t0 = pygame.time.get_ticks()

        self._status = status

    def shoot(self):
        if not self._is_shooting:
            self._is_shooting = True

    def display(self, screen):
        self._frame += 1

        if self._status == Blaster.MOVING:
            if self._direction == -1:
                self._v = max(self._v0 - Blaster.ACCELERATION * ((pygame.time.get_ticks() - self._t0)), -Blaster.MAX_SPEED)
            elif self._direction == 1:
                self._v = min(self._v0 + Blaster.ACCELERATION * ((pygame.time.get_ticks() - self._t0)), Blaster.MAX_SPEED)
        elif self._status == Blaster.STOPPING and self._t0 != -1:
            if self._direction == -1:
                self._v = min(self._v0 - Blaster.DECELERATION * ((pygame.time.get_ticks() - self._t0)), 0)
            elif self._direction == 1:
                self._v = max(self._v0 + Blaster.DECELERATION * ((pygame.time.get_ticks() - self._t0)), 0)

            if self._v == 0:
                self._status = Blaster.STOPPED

        self._angle += self._v

        sx = screen.get_width() / 2
        sy = screen.get_height() / 2
        dy = sin(radians(self._angle)) * Blaster.RADIUS
        dx = cos(radians(self._angle)) * Blaster.RADIUS

        if self._is_shooting and self._frame % 25 == 0:
            # Spawn bullet pew pew pew
            if self.blaster_gfx == self._default_blaster_gfx:
                self.bullets.append(Bullet(self.player, sx + dx * 2, sy + dy * 2, 270 - self._angle, 1))

            self.blaster_gfx = self._blaster.next()

            # Shooting action has stopped
            if self.blaster_gfx == self._default_blaster_gfx:
                self._is_shooting = False

        if self._frame == 100:
            self.los_gfx = self._los.next()
            self._frame = 0

        rotated_blaster = pygame.transform.rotate(self.blaster_gfx, 270 - self._angle)
        rotated_los = pygame.transform.rotate(self.los_gfx, 270 - self._angle)

        blaster_rect = rotated_blaster.get_rect(center=(sx + dx, sy + dy))
        los_rect = rotated_los.get_rect(center=(sx + dx * 2, sy + dy * 2))

        for b in self.bullets:
            b.display(screen)

        screen.blit(rotated_los, los_rect)
        screen.blit(rotated_blaster, blaster_rect)