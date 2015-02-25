import os
import pygame
import random


class Mirror:
    SCALE = 3
    IMAGES = [os.path.join("minigames/mirrors/images", f) for f in os.listdir("minigames/mirrors/images") if f.startswith("mirror") and os.path.isfile(os.path.join("minigames/mirrors/images", f))]
    ANGLES = [180, 270, 0, 90]

    def __init__(self, screen_size, mirrors):
        self.frame = 0.0
        self.hiding = False
        self.angle = random.choice(Mirror.ANGLES)
        self.position = (0, 0)
        self.gfx = pygame.image.load(random.choice(Mirror.IMAGES))
        self.gfx = pygame.transform.scale(self.gfx, (self.gfx.get_width() * Mirror.SCALE, self.gfx.get_height() * Mirror.SCALE))
        self.gfx = pygame.transform.rotate(self.gfx, self.angle)

        screen_width, screen_height = screen_size
        mirrors = filter(lambda m: m.angle == self.angle, mirrors)

        # Pop from Top
        if self.angle == 180:
            excluded_ranges = [range(m.x1, m.x1 + 2 * m.gfx.get_width()) for m in mirrors]
            self.x1 = self.random_position(self.gfx.get_width(), screen_width - self.gfx.get_width(), excluded_ranges)
            self.x2 = self.x1
            self.y1 = -self.gfx.get_height()
            self.y2 = 0
        # Pop from Right
        elif self.angle == 90:
            excluded_ranges = [range(m.y1, m.y1 + 2 * m.gfx.get_height()) for m in mirrors]
            self.x1 = screen_width
            self.x2 = screen_width - self.gfx.get_width()
            self.y1 = self.random_position(self.gfx.get_height(), screen_height - self.gfx.get_height(), excluded_ranges)
            self.y2 = self.y1
        # Pop from Bottom
        elif self.angle == 0:
            excluded_ranges = [range(m.x1, m.x1 + 2 * m.gfx.get_width()) for m in mirrors]
            self.x1 = self.random_position(self.gfx.get_width(), screen_width - self.gfx.get_width(), excluded_ranges)
            self.x2 = self.x1
            self.y1 = screen_height
            self.y2 = self.y1 - self.gfx.get_height()
        # Pop from Left
        elif self.angle == 270:
            excluded_ranges = [range(m.y1, m.y1 + 2 * m.gfx.get_height()) for m in mirrors]
            self.x1 = -self.gfx.get_width()
            self.x2 = 0
            self.y1 = self.random_position(self.gfx.get_height(), screen_height - self.gfx.get_height(), excluded_ranges)
            self.y2 = self.y1

    def random_position(self, min, max, excluded_ranges):
        positions = range(min, max)

        for p in positions:
            for er in excluded_ranges:
                if p in er:
                    positions.remove(p)
                    break

        return random.choice(positions)

    def destroy(self):
        pass

    def display(self, screen, speed, animation_duration, show_duration, bullets):
        for b in bullets:
            if b.collides_with(self):
                return b.owner

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
        screen.blit(self.gfx, self.position)

        return None

    def smooth_step(self, p1, p2, t, d, a):
        if p1 == p2:
            return p1

        x = t / d
        x = a * (x * x * (3 - 2 * x))

        return (p1 * x) + (p2 * (1 - x))