import random
import pygame

class Cutlery:
    def __init__(self, difficulty):
        self.cutleryType = random.randint(0,2)
        if self.cutleryType == 0:
            self.image = pygame.image.load("./res/img/cutleryFall/fork.png").convert_alpha()
        elif self.cutleryType == 1:
            self.image = pygame.image.load("./res/img/cutleryFall/knife.png").convert_alpha()
        elif self.cutleryType == 2:
            self.image = pygame.image.load("./res/img/cutleryFall/spoon.png").convert_alpha()

        self.buttonType = random.randint(0,4)
        if self.buttonType == 0:
            self.button = pygame.image.load("./res/img/cutleryFall/up.png").convert_alpha()
        elif self.buttonType == 1:
            self.button = pygame.image.load("./res/img/cutleryFall/right.png").convert_alpha()
        elif self.buttonType == 2:
            self.button = pygame.image.load("./res/img/cutleryFall/down.png").convert_alpha()
        elif self.buttonType == 3:
            self.button = pygame.image.load("./res/img/cutleryFall/left.png").convert_alpha()
        elif self.buttonType == 4:
            self.button = pygame.image.load("./res/img/cutleryFall/action.png").convert_alpha()

        self.difficulty = difficulty
        self.score = 0
        self.pos = [random.randint(50, 750), 0]
        self.speed = random.randint(1, difficulty + 1)
        self.destroy = False

    def update(self):
        if self.pos[1] >= 600:
            self.falled()
        else:
            self.pos[1] += self.speed

    def draw(self, screen):
        drawPos = [self.pos[0], self.pos[1]]
        drawPos[0] -= self.image.get_rect().w / 2
        drawPos[1] -= self.image.get_rect().h
        screen.blit(self.image, drawPos)
        drawPos[0] += self.image.get_rect().w /2 - self.button.get_rect().w / 2
        drawPos[1] += self.image.get_rect().h /2 - self.button.get_rect().h / 2
        screen.blit(self.button, drawPos)

    def checkButton(self, button):
        return not self.destroy and self.buttonType == button

    def slapped(self, side):
        self.destroy = True

    def falled(self):
        self.destroy = True

    def remove(self):
        return self.destroy