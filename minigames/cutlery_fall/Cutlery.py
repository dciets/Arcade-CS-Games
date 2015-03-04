import random
import pygame

class Cutlery:
    def __init__(self, difficulty):
        self.ROTATION_SPEED = 20
        self.FLY_OFF = 20

        self.cutleryType = random.randint(0,2)
        if self.cutleryType == 0:
            self.image = pygame.image.load("./res/img/cutleryFall/cutlery/fork.png").convert_alpha()
        elif self.cutleryType == 1:
            self.image = pygame.image.load("./res/img/cutleryFall/cutlery/knife.png").convert_alpha()
        elif self.cutleryType == 2:
            self.image = pygame.image.load("./res/img/cutleryFall/cutlery/spoon.png").convert_alpha()

        self.buttonType = random.randint(0,4)
        if self.buttonType == 0:
            self.button = pygame.image.load("./res/img/cutleryFall/button/up.png").convert_alpha()
        elif self.buttonType == 1:
            self.button = pygame.image.load("./res/img/cutleryFall/button/right.png").convert_alpha()
        elif self.buttonType == 2:
            self.button = pygame.image.load("./res/img/cutleryFall/button/down.png").convert_alpha()
        elif self.buttonType == 3:
            self.button = pygame.image.load("./res/img/cutleryFall/button/left.png").convert_alpha()
        elif self.buttonType == 4:
            self.button = pygame.image.load("./res/img/cutleryFall/button/action.png").convert_alpha()

        self.difficulty = difficulty
        self.score = 0
        self.rotation = 0
        self.rotDir = 0
        self.move = 0
        self.pos = [random.randint(50, 750), 0]
        self.speed = random.randint(6, difficulty + 6)
        self.active = True
        self.destroy = False
        self.visit = False

    def update(self):
        if not self.active:
            self.pos[1] -= 1
            self.pos[0] += self.move
            self.rotation += self.rotDir
            if self.pos[0] < 0 or self.pos[0] > 800:
                self.destroy = True
        elif self.pos[1] >= 600:
            self.falled()
        else:
            self.pos[1] += self.speed

    def draw(self, screen):
        newImage = pygame.transform.rotate(self.image, self.rotation)
        drawPos = [self.pos[0], self.pos[1]]
        drawPos[0] -= newImage.get_rect().w / 2
        drawPos[1] -= newImage.get_rect().h
        screen.blit(newImage, drawPos)
        if self.active:
            drawPos[0] += newImage.get_rect().w /2 - self.button.get_rect().w / 2
            drawPos[1] += newImage.get_rect().h /2 - self.button.get_rect().h / 2
            screen.blit(self.button, drawPos)

    def checkButton(self, button):
        return self.active and self.buttonType == button

    def slapped(self, side):
        self.move = -self.FLY_OFF if side == 0 else self.FLY_OFF
        self.rotDir = -self.ROTATION_SPEED if side == 0 else self.ROTATION_SPEED
        self.active = False

    def falled(self):
        side = random.randint(0,1)
        self.slapped(side)
        self.visit = True
