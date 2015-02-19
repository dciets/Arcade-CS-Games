import os
import pygame
import random
import operator
from minigames.mirrors.directions import Directions


class Mirror:
    SCALE = 5
    IMAGES = [ os.path.join("minigames/mirrors/images", f) for f in os.listdir("minigames/mirrors/images") if f.startswith("mirror") and os.path.isfile(os.path.join("minigames/mirrors/images", f)) ]

    def __init__(self, screen):
        self.screen = screen
        self.direction = Directions.random()
        self.img = pygame.image.load(random.choice(Mirror.IMAGES))
        self.img = pygame.transform.scale(self.img, map(operator.mul, self.img.get_size(), len(self.img.get_size()) * (Mirror.SCALE,)))
        self.img = pygame.transform.rotate(self.img, self.direction)

        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        if self.direction == Directions.TOP:
            self.position = (random.randint(self.img.get_width(), screen_width - self.img.get_width()), -screen_height)
        elif self.direction == Directions.RIGHT:
            self.position = (screen_width + self.img.get_width(), random.randint(self.img.get_height(), screen_height - self.img.get_height()))
        elif self.direction == Directions.BOTTOM:
            self.position = (random.randint(self.img.get_width(), screen_width - self.img.get_width()), screen_height + self.img.get_height())
        elif self.direction == Directions.LEFT:
            self.position = (-self.img.get_width(), random.randint(self.img.get_height(), screen_height - self.img.get_height()))

    def show(self):
        self.screen.blit(self.img, self.position)

        if self.direction == Directions.TOP:
            self.position = self.position = (self.position[0], self.position[1] + 10)
        elif self.direction == Directions.RIGHT:
            self.position = (self.position[0] - 10, self.position[1])
        elif self.direction == Directions.BOTTOM:
            self.position = (self.position[0], self.position[1] - 10)
        elif self.direction == Directions.LEFT:
            self.position = (self.position[0] + 10, self.position[1])