import pygame
import random

class Ring:
    def __init__(self, posX, posY, difficulty):
        self.difficulty = difficulty
        self.image = pygame.image.load("./res/img/stay_in_the_ring/ring.png").convert_alpha()
        self.pos = [posX, posY]
        self.scale = 1.0
        self.rect = self.image.get_rect()
        self.collisionBox = self.image.get_rect()
        self.updateRects()

        self.TELEPORT = 5
        self.KEEP_DIR_TIME = 0.25
        self.keepDirTime = 0.5
        self.dir = 0
        self.speed = difficulty * 1.5 + 6

    def update(self, timeElapsed):
        self.keepDirTime += timeElapsed
        self.move(dir)

        if self.scale > 0.05:
            self.scale -= (0.003 + 0.001 * self.difficulty)
        if self.scale <= 0.05:
            self.scale = 0.05
        self.updateRects()

    def draw(self, screen):
        image = pygame.transform.scale(self.image, (self.rect.w, self.rect.h))
        screen.blit(image, self.rect)

    def updateRects(self):
        size = self.image.get_size()
        self.rect.w = size[0] * self.scale
        self.rect.h = size[1] * self.scale
        self.rect.x = self.pos[0] - self.rect.w / 2
        self.rect.y = self.pos[1] - self.rect.h / 2
        self.collisionBox.x = self.rect.x + self.rect.w / 16
        self.collisionBox.y = self.rect.y + self.rect.h / 2 + self.rect.h / 16
        self.collisionBox.w = self.rect.w - self.rect.w / 8
        self.collisionBox.h = self.rect.h - self.rect.h / 2 - self.rect.h / 8

    def updatePos(self):
        if self.pos[0] < 25:
            self.pos[0] = 25
        elif self.pos[0] > 725:
            self.pos[0] = 725
        if self.pos[1] < 200:
            self.pos[1] = 200
        elif self.pos[1] > 525:
            self.pos[1] = 525

    def move(self, direction):
        if self.keepDirTime >= self.KEEP_DIR_TIME:
            self.keepDirTime = 0
            self.dir = random.randint(0,3)

        if self.dir == 0:
            self.pos[1] -= self.speed
        elif self.dir == 1:
            self.pos[0] -= self.speed
        elif self.dir == 2:
            self.pos[0] += self.speed
        elif self.dir == 3:
            self.pos[1] += self.speed

        if self.difficulty >= self.TELEPORT and random.randint(0, 1000) < 5:
            self.pos = [random.randint(25, 725), random.randint(200, 525)]

        self.updatePos()