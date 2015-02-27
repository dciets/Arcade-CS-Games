import pygame

class Coin:
    def __init__(self, pos):
        self.pos = [pos[0], pos[1]]
        self.moveBy = 100
        self.image = pygame.image.load("./res/img/leprechaunBeatemUp/Coin.png").convert_alpha()
        self.rect = self.image.get_rect()

    def update(self):
        self.pos[1] -= 1
        self.moveBy -= 1

    def draw(self, screen):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        screen.blit(self.image, self.rect)

    def end(self):
        return self.moveBy <= 0