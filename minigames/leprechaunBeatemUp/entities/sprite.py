import pygame

class Sprite:
    def __init__(self, path):
        self.NB_SPRITE = 3
        self.NB_IMG_PER_SPRITE = 4
        self.UPDATE_TIME = 0.1
        self.updateTime = 0

        self.path = path
        self.image = pygame.image.load(path).convert_alpha()
        self.flip = False
        self.spriteRect = pygame.Rect(0, 0, self.image.get_rect().w / self.NB_IMG_PER_SPRITE, self.image.get_rect().h / self.NB_SPRITE)
        self.rect = pygame.Rect(0, 0, self.image.get_rect().w / self.NB_IMG_PER_SPRITE, self.image.get_rect().h / self.NB_SPRITE)

    def update(self, elapsed):
        if self.updateTime >= self.UPDATE_TIME:
            self.updateTime = 0
            self.spriteRect.x += self.spriteRect.w
            if self.spriteRect.x >= self.image.get_rect().w:
                self.spriteRect.x = 0
        else:
            self.updateTime += elapsed

    def changeSprite(self, sprite):
        if sprite == "normal":
            self.spriteRect.y = 0 * self.spriteRect.h
        elif sprite == "left":
            self.spriteRect.y = 1 * self.spriteRect.h
            self.flip = True
        elif sprite == "right":
            self.spriteRect.y = 1 * self.spriteRect.h
            self.flip = False
        elif sprite == "action":
            self.spriteRect.y = 2 * self.spriteRect.h

    def draw(self, screen, pos):
        self.rect.x = pos[0] - self.rect.w/2
        self.rect.y = pos[1] - self.rect.h/2
        if self.flip:
            screen.blit(pygame.transform.flip(self.image,1,0), self.rect, self.spriteRect)
        else:
            screen.blit(self.image, self.rect, self.spriteRect)
