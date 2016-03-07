import pygame

class Ring:
    def __init__(self, posX, posY, difficulty):
        self.difficulty = difficulty
        self.image = pygame.image.load("./res/img/stay_in_the_ring/ring.png").convert_alpha()
        self.center = [posX, posY]
        self.scale = 1.0
        self.rect = self.image.get_rect()
        self.collisionBox = self.image.get_rect()
        self.updateRects()

    def update(self):
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
        self.rect.x = self.center[0] - self.rect.w / 2
        self.rect.y = self.center[1] - self.rect.h / 2
        self.collisionBox.x = self.rect.x + self.rect.w / 16
        self.collisionBox.y = self.rect.y + self.rect.h / 2 + self.rect.h / 16
        self.collisionBox.w = self.rect.w - self.rect.w / 8
        self.collisionBox.h = self.rect.h - self.rect.h / 2 - self.rect.h / 8