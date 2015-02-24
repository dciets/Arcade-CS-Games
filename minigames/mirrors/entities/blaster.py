from math import sin, radians, cos
from itertools import cycle
import random
import pygame


class Blaster:
    SCALE = 2
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
        self.angle = random.randint(0, 359)
        self.shooting = False

        for path in Blaster.BLASTER_SPRITES[player]:
            img = pygame.image.load(path)
            img = pygame.transform.scale(img, (img.get_width() * Blaster.SCALE, img.get_height() * Blaster.SCALE))
            self.blaster_gfx.append(img)

        for path in Blaster.LOS_SPRITES[player]:
            img = pygame.image.load(path)
            #img = pygame.transform.scale(img, (img.get_width() * Blaster.SCALE, img.get_height() * Blaster.SCALE))
            self.los_gfx.append(img)

        self.los_gfx = cycle(self.los_gfx)

    def display(self, screen):
        sx = screen.get_width() / 2
        sy = screen.get_height() / 2
        dy = sin(radians(self.angle)) * Blaster.RADIUS
        dx = cos(radians(self.angle)) * Blaster.RADIUS

        rotated_gfx = pygame.transform.rotate(self.blaster_gfx[self.frame], 270 - self.angle)
        rect = rotated_gfx.get_rect(center=(sx + dx, sy + dy))

        screen.blit(rotated_gfx, rect)