import os
import pygame
import random
import operator
from minigames.mirrors.borders import Borders


class Mirror:
    SCALE = 3
    IMAGES = [os.path.join("minigames/mirrors/images", f) for f in os.listdir("minigames/mirrors/images") if f.startswith("mirror") and os.path.isfile(os.path.join("minigames/mirrors/images", f))]

    def __init__(self, screen_size):
        self.frame = 0.0
        self.hiding = False
        self.direction = Borders.random()
        self.position = (0, 0)
        self.img = pygame.image.load(random.choice(Mirror.IMAGES))
        self.img = pygame.transform.scale(self.img, map(operator.mul, self.img.get_size(), len(self.img.get_size()) * (Mirror.SCALE,)))
        self.img = pygame.transform.rotate(self.img, self.direction)

        screen_width, screen_height = screen_size

        if self.direction == Borders.TOP:
            self.x1 = random.randint(self.img.get_width(), screen_width - self.img.get_width())
            self.x2 = self.x1
            self.y1 = -self.img.get_height()
            self.y2 = 0
        elif self.direction == Borders.RIGHT:
            self.x1 = screen_width
            self.x2 = screen_width - self.img.get_width()
            self.y1 = random.randint(self.img.get_height(), screen_height - self.img.get_height())
            self.y2 = self.y1
        elif self.direction == Borders.BOTTOM:
            self.x1 = random.randint(self.img.get_width(), screen_width - self.img.get_width())
            self.x2 = self.x1
            self.y1 = screen_height
            self.y2 = self.y1 - self.img.get_height()
        elif self.direction == Borders.LEFT:
            self.x1 = -self.img.get_width()
            self.x2 = 0
            self.y1 = random.randint(self.img.get_height(), screen_height - self.img.get_height())
            self.y2 = self.y1

    def show(self, screen, speed, animation_duration, show_duration):
        if self.frame <= animation_duration:
            if not self.hiding:
                self.position = (self.smooth_step(self.x1, self.x2, animation_duration - self.frame, animation_duration, speed), self.smooth_step(self.y1, self.y2, animation_duration - self.frame, animation_duration, speed))
            else:
                self.position = (self.smooth_step(self.x1, self.x2, self.frame, animation_duration, speed), self.smooth_step(self.y1, self.y2, self.frame, animation_duration, speed))

        elif self.frame == animation_duration + show_duration and not self.hiding:
            self.hiding = True
            self.frame = 0.0
            speed *= 10

        self.frame += 1.0
        screen.blit(self.img, self.position)

    def smooth_step(self, p1, p2, t, d, a):
        if p1 == p2:
            return p1

        x = t / d
        x = a * (x * x * (3 - 2 * x))

        return (p1 * x) + (p2 * (1 - x))