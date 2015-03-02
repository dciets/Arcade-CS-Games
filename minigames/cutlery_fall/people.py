import pygame
import random

class People:
    def __init__(self, type, pos):
        i = random.randint(1,3)
        if type == 0:
            self.image = pygame.image.load("./res/img/cutleryFall/woman/woman" + str(i) + ".png").convert_alpha()
        elif type == 1:
            self.image = pygame.image.load("./res/img/cutleryFall/man/man" + str(i) + ".png").convert_alpha()
        elif type == 2:
            self.image = pygame.image.load("./res/img/cutleryFall/child/child" + str(i) + ".png").convert_alpha()

        self.pos = [400 - self.image.get_rect().w / 2 + pos, 300 - self.image.get_rect().h / 2]

    def draw(self, screen):
        screen.blit(self.image, self.pos)