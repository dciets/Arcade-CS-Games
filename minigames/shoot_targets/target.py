import random
import pygame
import operator


class Target:

    image = pygame.image.load('res/img/shoot_targets/target.png')
    center = map(lambda x: x / 2, image.get_rect().size)

    def __init__(self, parent, position=[0, 0]):
        self.parent = parent
        self.position = position
        self.hitbox_radius = 31
        self.hit = False
        # self.velocity = [0, 0]

    def update(self):
        # self.position = map(operator.add, self.position, self.velocity)
        pass

    def render(self):
        self.parent.screen.blit(Target.image, map(operator.sub, self.position, Target.center))
