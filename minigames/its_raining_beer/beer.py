import pygame
from pygame.sprite import Sprite


class Beer(Sprite):
    IMAGE_DIRECTORY = "res/img/its_raining_beer/"

    def __init__(self, position, width, speed, *groups):
        super(Beer, self).__init__(*groups)
        self.x, self.y = position
        self.speed = speed
        image = pygame.image.load(self.IMAGE_DIRECTORY + "beer.png").convert_alpha()
        height2 = int((float(image.get_height()) / image.get_width()) * width)
        self.image = pygame.transform.scale(image, (width, height2))
        self.width, self.height = self.image.get_size()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.y += self.speed
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def blit(self, screen):
        screen.blit(self.image, (self.x, self.y))


