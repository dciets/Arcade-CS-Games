import os
import pygame
import random


class Mirror:
    SCALE = 3
    ANIMATION_DURATION = 150
    BASE_SPEED = 3
    IMAGES = [os.path.join("minigames/mirrors/images", f) for f in os.listdir("minigames/mirrors/images") if f.startswith("mirror") and os.path.isfile(os.path.join("minigames/mirrors/images", f))]
    ANGLES = [180, 270, 0, 90]

    def __init__(self, screen_size, show_duration, mirrors):
        self.speed = Mirror.BASE_SPEED
        self.show_duration = show_duration
        self.frame = 0.0
        self.hiding = False
        self.destroyed = False
        self.blink_count = 0
        self.angle = random.choice(Mirror.ANGLES)
        self.position = (0, 0)
        self.gfx = pygame.image.load(random.choice(Mirror.IMAGES))
        self.gfx = pygame.transform.scale(self.gfx, (self.gfx.get_width() * Mirror.SCALE, self.gfx.get_height() * Mirror.SCALE))
        self.gfx = pygame.transform.rotate(self.gfx, self.angle)

        screen_width, screen_height = screen_size
        mirrors = filter(lambda m: m.angle == self.angle, mirrors)

        self._initial_position = None

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

        for i, p in enumerate(positions):
            for er in excluded_ranges:
                if p in er:
                    del positions[i]
                    break

        return random.choice(positions)

    def is_visible(self):
        x, y = self.position

        return not (self.hiding and self.position == self._initial_position)

    def destroy(self):
        self.destroyed = True

    def display(self, screen):
        if self.destroyed:
            if self.frame % 25 == 0:
                self.blink_count += 1

            # Blink 6 times, then reset to original position (to hide and delete the mirror)
            if self.blink_count == 6:
                self.position = self._initial_position
        else:
            if self.frame <= Mirror.ANIMATION_DURATION:
                if not self.hiding:
                    self.position = (self.smooth_step(self.x1, self.x2, Mirror.ANIMATION_DURATION - self.frame, Mirror.ANIMATION_DURATION), self.smooth_step(self.y1, self.y2, Mirror.ANIMATION_DURATION - self.frame, Mirror.ANIMATION_DURATION))
                else:
                    self.position = (self.smooth_step(self.x1, self.x2, self.frame, Mirror.ANIMATION_DURATION), self.smooth_step(self.y1, self.y2, self.frame, Mirror.ANIMATION_DURATION))

            if self._initial_position == None:
                self._initial_position = self.position

            elif self.frame == Mirror.ANIMATION_DURATION + self.show_duration and not self.hiding:
                self.hiding = True
                self.frame = 0.0
                self.speed *= 10

        self.frame += 1.0

        if self.blink_count % 2 == 0:
            screen.blit(self.gfx, self.position)

    def smooth_step(self, p1, p2, t, d):
        if p1 == p2:
            return p1

        x = t / d
        x = self.speed * (x * x * (3 - 2 * x))

        return (p1 * x) + (p2 * (1 - x))