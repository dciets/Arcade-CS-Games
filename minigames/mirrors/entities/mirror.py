import os
import pygame
import random


class Mirror:
    SCALE = 3

    SHOWING = 0
    WAITING = 1
    HIDING = 2
    DESTROYED = 3

    SHOW_ANIMATION_DURATION = 25
    HIDE_ANIMATION_DURATION = 10
    DESTROY_ANIMATION_FREQUENCY = 4

    IMAGES = [os.path.join("minigames/mirrors/images", f) for f in os.listdir("minigames/mirrors/images") if f.startswith("mirror") and os.path.isfile(os.path.join("minigames/mirrors/images", f))]
    ANGLES = [180, 270, 0, 90]

    def __init__(self, game, screen_size, duration, mirrors):
        self.game = game
        self.show_animation_duration = max(Mirror.SHOW_ANIMATION_DURATION / (self.game.difficulty + 1), 10)

        self.spawn_start_frame = self.game.frame
        self.animation_start_frame = self.spawn_start_frame
        self.destroy_start_frame = 0

        self.status = Mirror.SHOWING
        self.blink = False
        self.duration = duration
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
        return self.game.frame - self.spawn_start_frame < self.show_animation_duration + self.duration + Mirror.HIDE_ANIMATION_DURATION

    def destroy(self):
        self.destroy_start_frame = self.game.elapsed_ms
        self.status = Mirror.DESTROYED

    def display(self, screen):
        if self.is_visible():
            x1 = 0
            x2 = 0
            y1 = 0
            y2 = 0
            d = 1

            if self.game.frame - self.spawn_start_frame < self.show_animation_duration:
                x1 = self.x1
                x2 = self.x2
                y1 = self.y1
                y2 = self.y2
                d = self.show_animation_duration
            elif self.show_animation_duration <= self.game.frame - self.spawn_start_frame < self.show_animation_duration + self.duration:
                if self.status == Mirror.SHOWING:
                    self.animation_start_frame = self.game.frame
                    self.status = Mirror.WAITING

                x1 = self.x2
                x2 = self.x2
                y1 = self.y2
                y2 = self.y2
                d = self.duration
            else:
                if self.status == Mirror.WAITING:
                    self.animation_start_frame = self.game.frame
                    self.status = Mirror.HIDING

                x1 = self.x2
                x2 = self.x1
                y1 = self.y2
                y2 = self.y1
                d = Mirror.HIDE_ANIMATION_DURATION

            x = int(self.smooth_step(x1, x2, self.game.frame - self.animation_start_frame, d) + 0.5)
            y = int(self.smooth_step(y1, y2, self.game.frame - self.animation_start_frame, d) + 0.5)
            self.position = (x, y)

            if self._initial_position is None:
                self._initial_position = self.position

            if self.game.frame % Mirror.DESTROY_ANIMATION_FREQUENCY == 0:
                self.blink = not self.blink

            if self.status != Mirror.DESTROYED or not self.blink:
                screen.blit(self.gfx, self.position)

    def smooth_step(self, p1, p2, t, d):
        if p1 == p2:
            return p1

        x = (float(t) / float(d))
        x = (x * x * (3 - 2 * x))

        return (p2 * x) + (p1* (1 - x))