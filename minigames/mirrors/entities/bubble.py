import operator
import pygame


class Bubble:
    SCALE = 4

    def __init__(self):
        sprite1 = pygame.image.load("minigames/mirrors/images/bubble1.png")
        sprite1 = pygame.transform.scale(sprite1, map(operator.mul, sprite1.get_size(), len(sprite1.get_size()) * (Bubble.SCALE,)))
        sprite2 = pygame.image.load("minigames/mirrors/images/bubble2.png")
        sprite2 = pygame.transform.scale(sprite2, map(operator.mul, sprite2.get_size(), len(sprite2.get_size()) * (Bubble.SCALE,)))

        self.frame = 1
        self.state = 0
        self.sprites = [sprite1, sprite2]

    def animate(self, screen):
        if self.frame % 500 == 0:
            self.state = 0
            self.frame = 1
        elif self.frame % 250 == 0:
            self.state = 1

        screen.blit(self.sprites[self.state], ((screen.get_width() / 2) - (self.sprites[self.state].get_width() / 2), (screen.get_height() / 2) - (self.sprites[self.state].get_height() / 2)))
        self.frame += 1