import pygame
from minigames.mirrors.entities.blaster import Blaster
import random


class BlasterBase:
    SCALE = 8

    def __init__(self, num_players):
        self.blasters = []
        self.gfx = pygame.image.load("minigames/mirrors/images/blaster_base.png")
        self.gfx = pygame.transform.scale(self.gfx, (self.gfx.get_width() * BlasterBase.SCALE, self.gfx.get_height() * BlasterBase.SCALE))

        for player in range(0, num_players):
            self.blasters.append(Blaster(player))

    def get_bullets(self):
        bullets = []

        for blaster in self.blasters:
            for bullet in blaster.bullets:
                bullets.append(bullet)

        return bullets

    def display(self, screen):
        b = self.blasters[:]
        random.shuffle(b)

        while len(b) > 0:
            b.pop().display(screen)

        screen.blit(self.gfx, ((screen.get_width() / 2) - (self.gfx.get_width() / 2), (screen.get_height() / 2) - (self.gfx.get_height() / 2)))