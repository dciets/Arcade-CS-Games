from math import sin, radians, cos
from itertools import cycle
import random
import pygame
from minigames.mirrors.entities.bullet import Bullet


class Blaster:
    MAX_SPEED = 2
    MAX_POWER = 4.0
    ACCELERATION = 0.005
    DECELERATION = -0.005

    # Blaster status
    MOTION = 0
    ACTION = 1
    IDLE = 0
    # Motions
    DECELERATING = 1
    ACCELERATING = 2
    # Actions
    CHARGING = 1
    SHOOTING = 2

    LEFT = -1
    RIGHT = 1
    RADIUS = 70
    BLASTER_SPRITES = [ ["minigames/mirrors/images/blaster1_1.png",
                         "minigames/mirrors/images/blaster1_2.png",
                         "minigames/mirrors/images/blaster1_3.png",
                         "minigames/mirrors/images/blaster1_4.png"],
                        ["minigames/mirrors/images/blaster2_1.png",
                         "minigames/mirrors/images/blaster2_2.png",
                         "minigames/mirrors/images/blaster2_3.png",
                         "minigames/mirrors/images/blaster2_4.png"] ]
    EXPLOSION_SPRITES = [ "minigames/mirrors/images/poof1.png",
                          "minigames/mirrors/images/poof2.png",
                          "minigames/mirrors/images/poof3.png",
                          "minigames/mirrors/images/poof4.png",
                          "minigames/mirrors/images/poof5.png",
                          "minigames/mirrors/images/poof6.png",
                          "minigames/mirrors/images/poof7.png",
                          "minigames/mirrors/images/poof8.png"]
    LOS_SPRITES = [ ["minigames/mirrors/images/los1_1.png",
                     "minigames/mirrors/images/los1_2.png"],
                    ["minigames/mirrors/images/los2_1.png",
                     "minigames/mirrors/images/los2_2.png"] ]

    def __init__(self, game, player):
        self.game = game

        self._frame = 0
        self._t0 = -1
        self._v0 = 0
        self._v = 0
        self._status = [Blaster.IDLE, Blaster.IDLE]
        self._angle = random.randint(0, 359)
        self._direction = Blaster.RIGHT

        self.bullets = []
        self.player = player
        self.power = 1.0

        # GFX
        self._blaster = [
            cycle([ pygame.image.load(Blaster.BLASTER_SPRITES[player][0]).convert_alpha(),
                    pygame.image.load(Blaster.BLASTER_SPRITES[player][1]).convert_alpha(),
                    pygame.image.load(Blaster.BLASTER_SPRITES[player][2]).convert_alpha(),
                    pygame.image.load(Blaster.BLASTER_SPRITES[player][1]).convert_alpha() ]),
            cycle([ pygame.image.load(Blaster.BLASTER_SPRITES[player][2]).convert_alpha(),
                    pygame.image.load(Blaster.BLASTER_SPRITES[player][3]).convert_alpha() ])
        ]
        self._los = cycle([ pygame.image.load(Blaster.LOS_SPRITES[player][0]).convert_alpha(),
                            pygame.image.load(Blaster.LOS_SPRITES[player][1]).convert_alpha() ])
        self._explosion = cycle([ pygame.image.load(Blaster.EXPLOSION_SPRITES[0]).convert_alpha(),
                                  pygame.image.load(Blaster.EXPLOSION_SPRITES[1]).convert_alpha(),
                                  pygame.image.load(Blaster.EXPLOSION_SPRITES[2]).convert_alpha(),
                                  pygame.image.load(Blaster.EXPLOSION_SPRITES[3]).convert_alpha(),
                                  pygame.image.load(Blaster.EXPLOSION_SPRITES[4]).convert_alpha(),
                                  pygame.image.load(Blaster.EXPLOSION_SPRITES[5]).convert_alpha(),
                                  pygame.image.load(Blaster.EXPLOSION_SPRITES[6]).convert_alpha(),
                                  pygame.image.load(Blaster.EXPLOSION_SPRITES[7]).convert_alpha() ])

        self._idle_blaster_gfx = self.blaster_gfx = self._blaster[0].next()
        self.los_gfx = self._los.next()
        self.explosion_gfx = self._explosion.next()

    def set_direction(self, direction):
        self._direction = direction
        self._v0 = self._v

    def set_motion(self, status):
        if self._status[Blaster.MOTION] != status:
            self._v0 = self._v
            self._t0 = pygame.time.get_ticks()

        self._status[Blaster.MOTION] = status

    def set_action(self, status):
        self._charge_mode = 0
        self._status[Blaster.ACTION] = status

    def do_motion(self):
        if self._status[Blaster.MOTION] == Blaster.ACCELERATING:
            if self._direction == -1:
                self._v = max(self._v0 - Blaster.ACCELERATION * ((pygame.time.get_ticks() - self._t0)), -Blaster.MAX_SPEED)
            elif self._direction == 1:
                self._v = min(self._v0 + Blaster.ACCELERATION * ((pygame.time.get_ticks() - self._t0)), Blaster.MAX_SPEED)
        elif self._status[Blaster.MOTION] == Blaster.DECELERATING and self._t0 != -1:
            if self._direction == -1:
                self._v = min(self._v0 - Blaster.DECELERATION * ((pygame.time.get_ticks() - self._t0)), 0)
            elif self._direction == 1:
                self._v = max(self._v0 + Blaster.DECELERATION * ((pygame.time.get_ticks() - self._t0)), 0)

            if self._v == 0:
                self._status[Blaster.MOTION] = Blaster.IDLE

        self._angle += self._v

    def do_action(self, x, y):
        if self._status[Blaster.ACTION] == Blaster.CHARGING:
            if self._frame % 50 == 0:
                if self.power < 2:
                    self.blaster_gfx = self._blaster[0].next()

                self.power = min(self.power + 0.5, Blaster.MAX_POWER)
            elif self.power == Blaster.MAX_POWER and self._frame % 15 == 0:
                self.blaster_gfx = self._blaster[1].next()
        elif self._status[Blaster.ACTION] == Blaster.SHOOTING and self._frame % 25 == 0:
            self.blaster_gfx = self._blaster[0].next()

            if self.blaster_gfx == self._idle_blaster_gfx:
                self.bullets.append(Bullet(self.game, self.player, x, y, 270 - self._angle, self.power))
                self._status[Blaster.ACTION] = Blaster.IDLE
                self.power = 1

    def display(self, screen):
        if self._frame == 100:
            self.los_gfx = self._los.next()
            self._frame = 1
        else:
            self._frame += 1

        sx = screen.get_width() / 2
        sy = screen.get_height() / 2
        dy = sin(radians(self._angle)) * Blaster.RADIUS
        dx = cos(radians(self._angle)) * Blaster.RADIUS

        self.do_motion()
        self.do_action(sx + dx, sy + dy)

        rotated_blaster = pygame.transform.rotate(self.blaster_gfx, 270 - self._angle)
        rotated_los = pygame.transform.rotate(self.los_gfx, 270 - self._angle)

        blaster_rect = rotated_blaster.get_rect(center=(sx + dx, sy + dy))
        los_rect = rotated_los.get_rect(center=(sx + dx, sy + dy))

        for i, b in enumerate(self.bullets):
            if not b.is_visible(screen):
                del self.bullets[i]
            else:
                b.display(screen)

        screen.blit(rotated_los, los_rect)
        screen.blit(rotated_blaster, blaster_rect)