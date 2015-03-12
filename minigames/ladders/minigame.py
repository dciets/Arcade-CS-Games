from itertools import cycle
import pygame
import random
from pygame.rect import Rect
from minigames import minigame


class LaddersMinigame(minigame.Minigame):
    name = "Evade the bees!"
    game_type = minigame.MULTIPLAYER
    max_duration = 10000

    BEE_BASE_SPEED = 10
    BEE_BASE_COUNT = 6

    def __init__(self, game):
        minigame.Minigame.__init__(self, game)

        self.game = game

        # Background GFX
        self.gfx_bg1 = pygame.image.load("./res/img/ladders/bg1.png")
        self.gfx_bg2 = pygame.image.load("./res/img/ladders/bg2.png")
        self.gfx_bg3 = pygame.image.load("./res/img/ladders/bg3.png")
        self.gfx_ladder = pygame.image.load("./res/img/ladders/ladder.png")

        # Entities GFX
        self.gfx_left_bee = cycle([
            pygame.transform.flip(pygame.image.load("./res/img/ladders/bee.png").subsurface(Rect((0, 0), (47, 49))), True),
            pygame.transform.flip(pygame.image.load("./res/img/ladders/bee.png").subsurface(Rect((54, 0), (47, 49))), True),
            pygame.transform.flip(pygame.image.load("./res/img/ladders/bee.png").subsurface(Rect((108, 0), (47, 49))), True),
            pygame.transform.flip(pygame.image.load("./res/img/ladders/bee.png").subsurface(Rect((54, 0), (47, 49))), True)
        ])
        self.gfx_right_bee = cycle([
            pygame.image.load("./res/img/ladders/bee.png").subsurface(Rect((0, 0), (47, 49))),
            pygame.image.load("./res/img/ladders/bee.png").subsurface(Rect((54, 0), (47, 49))),
            pygame.image.load("./res/img/ladders/bee.png").subsurface(Rect((108, 0), (47, 49))),
            pygame.image.load("./res/img/ladders/bee.png").subsurface(Rect((54, 0), (47, 49)))
        ])

        # Entities
        self.bees = ([], [])

    def init(self):
        for i in range(LaddersMinigame.BEE_BASE_COUNT / 2):
            self.bees[0].append((self.gfx_left_bee, random.randint(150, 500)))
            self.bees[1].append((self.gfx_left_bee, random.randint(150, 500)))

    def tick(self):
        # if self.frame % 2 == 0:
        #     self.bees = self.gfx_bee.next()

        self.game.screen.blit(self.gfx_bg2, (-2 * (self.frame % 319), 0))
        self.game.screen.blit(self.gfx_bg1, (20, 0))
        self.game.screen.blit(self.gfx_ladder, (self.game.GAME_WIDTH / 2 - 75, 100))
        self.game.screen.blit(self.gfx_ladder, (self.game.GAME_WIDTH / 2 + 75, 100))
        # self.game.screen.blit(self.bees, (100, 100))
        self.game.screen.blit(self.gfx_bg3, (-8 * (self.frame % 159), 0))
