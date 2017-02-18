import pygame
import math

class Player:
    def __init__(self, parent, index):
        self.parent = parent
        self.jumping = False
        self.index = index
        self.size = 50
        self.x = parent.screen_rect[0] * (0.4 + 0.2 * index) - self.size / 2
        self.y = parent.screen_rect[1] * 0.5 + parent.amplitude - self.size - 5
        self.jump_position = 0
        self.jump_start = 0
        self.fill = [(255, 0, 0), (0, 0, 255)][index]
        self.points = 0
        self.flag = False

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.jump_start = self.parent.elapsed_ms

    def update(self):
        t = (self.parent.elapsed_ms - self.jump_start)

        if self.jumping:
            if t > 500:
                self.jumping = False
                self.jump_position = 0
            else:
                self.jump_position = -50 * math.sin(t * math.pi / 500.0)


        if not self.jumping and not self.flag and self.parent.hittest():
            self.points -= 1
            self.flag = True

        if not self.parent.hittest():
            self.flag = False


    def render(self):
        pygame.draw.rect(self.parent.screen, self.fill, (self.x, self.y + self.jump_position, self.size, self.size))
