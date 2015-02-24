from itertools import cycle
import pygame


class Bubble:
    SCALE = 3

    def __init__(self):
        self.sprites = [pygame.image.load("minigames/mirrors/images/bubble1.png"),
                        pygame.image.load("minigames/mirrors/images/bubble2.png")]

        self.sprites[0] = pygame.transform.scale(self.sprites[0], (self.sprites[0].get_width() * Bubble.SCALE, self.sprites[0].get_height() * Bubble.SCALE))
        self.sprites[1] = pygame.transform.scale(self.sprites[1], (self.sprites[1].get_width() * Bubble.SCALE, self.sprites[1].get_height() * Bubble.SCALE))

        self.sprites = cycle(self.sprites)
        self.gfx = self.sprites.next()

    def display(self, screen):
        if pygame.time.get_ticks() % 250 == 0:
            self.gfx = self.sprites.next()

        screen.blit(self.gfx, ((screen.get_width() / 2) - (self.gfx.get_width() / 2), (screen.get_height() / 2) - (self.gfx.get_height() / 2)))