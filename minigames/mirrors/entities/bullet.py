from math import *
import pygame


class Bullet:
    SCALE = 3
    BASE_SPEED = 0.6
    BULLET_SPRITES = [ "minigames/mirrors/images/bullet1.png",
                       "minigames/mirrors/images/bullet2.png" ]
    def __init__(self, player, initial_x, initial_y, angle, power):
        self.gfx = pygame.image.load(Bullet.BULLET_SPRITES[player])
        self.gfx = pygame.transform.scale(self.gfx, (self.gfx.get_width() * Bullet.SCALE, self.gfx.get_height() * Bullet.SCALE))
        self.gfx = pygame.transform.rotate(self.gfx, angle)

        self._d = 0
        self._x0 = initial_x
        self._y0 = initial_y
        self._a = angle
        self._v = power * Bullet.BASE_SPEED

    def display(self, screen):
        self._d += self._v
        dx = self._d * sin(self._a)
        dy = self._d * cos(self._a)

        screen.blit(self.gfx, (self._x0 + dx, self._y0 + dy))