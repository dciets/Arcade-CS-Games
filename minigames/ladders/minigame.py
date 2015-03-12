from itertools import cycle
import pygame
import random
from pygame.rect import Rect
from minigames import minigame


SPRITE = 0
ANIMATION = 1

STILL_STATE = 0
UP_STATE = 1
DOWN_STATE = 2


class LaddersMinigame(minigame.Minigame):
    name = "Evade the bees!"
    game_type = minigame.MULTIPLAYER
    max_duration = 60000

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

        p = lambda x: x * 41 + x * 6
        # Entities GFX
        self.gfx_monkeys = [
            [
                cycle([pygame.image.load("./res/img/ladders/p1.png").subsurface(Rect((0, 0), (40, 35)))]),
                cycle([
                    pygame.image.load("./res/img/ladders/p1.png").subsurface(Rect((p(0), 50), (40, 47))),
                    pygame.image.load("./res/img/ladders/p1.png").subsurface(Rect((p(1), 50), (40, 47))),
                    pygame.image.load("./res/img/ladders/p1.png").subsurface(Rect((p(2), 50), (40, 47))),
                    pygame.image.load("./res/img/ladders/p1.png").subsurface(Rect((p(3), 50), (40, 47))),
                    pygame.image.load("./res/img/ladders/p1.png").subsurface(Rect((p(4), 50), (40, 47))),
                    pygame.image.load("./res/img/ladders/p1.png").subsurface(Rect((p(5), 50), (40, 47))),
                    pygame.image.load("./res/img/ladders/p1.png").subsurface(Rect((p(6), 50), (40, 47))),
                    pygame.image.load("./res/img/ladders/p1.png").subsurface(Rect((p(7), 50), (40, 47)))
                ]),
                cycle([
                    pygame.image.load("./res/img/ladders/p1.png").subsurface(Rect((p(0), 113), (40, 36))),
                    pygame.image.load("./res/img/ladders/p1.png").subsurface(Rect((p(1), 113), (40, 36))),
                    pygame.image.load("./res/img/ladders/p1.png").subsurface(Rect((p(2), 113), (40, 36))),
                    pygame.image.load("./res/img/ladders/p1.png").subsurface(Rect((p(3), 113), (40, 36))),
                    pygame.image.load("./res/img/ladders/p1.png").subsurface(Rect((p(4), 113), (40, 36))),
                    pygame.image.load("./res/img/ladders/p1.png").subsurface(Rect((p(5), 113), (40, 36))),
                    pygame.image.load("./res/img/ladders/p1.png").subsurface(Rect((p(6), 113), (40, 36))),
                    pygame.image.load("./res/img/ladders/p1.png").subsurface(Rect((p(7), 113), (40, 36)))
                ])
            ],
            [
               cycle([pygame.image.load("./res/img/ladders/p2.png").subsurface(Rect((0, 0), (40, 35)))]),
                cycle([
                    pygame.image.load("./res/img/ladders/p2.png").subsurface(Rect((p(0), 50), (40, 47))),
                    pygame.image.load("./res/img/ladders/p2.png").subsurface(Rect((p(1), 50), (40, 47))),
                    pygame.image.load("./res/img/ladders/p2.png").subsurface(Rect((p(2), 50), (40, 47))),
                    pygame.image.load("./res/img/ladders/p2.png").subsurface(Rect((p(3), 50), (40, 47))),
                    pygame.image.load("./res/img/ladders/p2.png").subsurface(Rect((p(4), 50), (40, 47))),
                    pygame.image.load("./res/img/ladders/p2.png").subsurface(Rect((p(5), 50), (40, 47))),
                    pygame.image.load("./res/img/ladders/p2.png").subsurface(Rect((p(6), 50), (40, 47))),
                    pygame.image.load("./res/img/ladders/p2.png").subsurface(Rect((p(7), 50), (40, 47)))
                ]),
                cycle([
                    pygame.image.load("./res/img/ladders/p2.png").subsurface(Rect((p(0), 113), (40, 36))),
                    pygame.image.load("./res/img/ladders/p2.png").subsurface(Rect((p(1), 113), (40, 36))),
                    pygame.image.load("./res/img/ladders/p2.png").subsurface(Rect((p(2), 113), (40, 36))),
                    pygame.image.load("./res/img/ladders/p2.png").subsurface(Rect((p(3), 113), (40, 36))),
                    pygame.image.load("./res/img/ladders/p2.png").subsurface(Rect((p(4), 113), (40, 36))),
                    pygame.image.load("./res/img/ladders/p2.png").subsurface(Rect((p(5), 113), (40, 36))),
                    pygame.image.load("./res/img/ladders/p2.png").subsurface(Rect((p(6), 113), (40, 36))),
                    pygame.image.load("./res/img/ladders/p2.png").subsurface(Rect((p(7), 113), (40, 36)))
                ])
            ]
        ]
        self.gfx_bees = [
            cycle([
                pygame.transform.flip(pygame.image.load("./res/img/ladders/bee.png").subsurface(Rect((0, 0), (47, 49))), True, False),
                pygame.transform.flip(pygame.image.load("./res/img/ladders/bee.png").subsurface(Rect((54, 0), (47, 49))), True, False),
                pygame.transform.flip(pygame.image.load("./res/img/ladders/bee.png").subsurface(Rect((108, 0), (47, 49))), True, False),
                pygame.transform.flip(pygame.image.load("./res/img/ladders/bee.png").subsurface(Rect((54, 0), (47, 49))), True, False)
            ]),
            cycle([
                pygame.image.load("./res/img/ladders/bee.png").subsurface(Rect((0, 0), (47, 49))),
                pygame.image.load("./res/img/ladders/bee.png").subsurface(Rect((54, 0), (47, 49))),
                pygame.image.load("./res/img/ladders/bee.png").subsurface(Rect((108, 0), (47, 49))),
                pygame.image.load("./res/img/ladders/bee.png").subsurface(Rect((54, 0), (47, 49)))
            ])
        ]

        # Entities
        self.monkeys = []
        self.bees = ([], [])
        # Triforce! ---^

    def init(self):
        self.monkeys = [
            [self.gfx_monkeys[0][STILL_STATE].next(), self.gfx_monkeys[0]],
            [self.gfx_monkeys[1][STILL_STATE].next(), self.gfx_monkeys[1]]
        ]

        for i in range(LaddersMinigame.BEE_BASE_COUNT / 2):
            self.bees[0].append((self.gfx_bees[0], random.randint(150, 500)))
            self.bees[1].append((self.gfx_bees[1], random.randint(150, 500)))

    def tick(self):
        if self.frame % 2 == 0:
            self.monkeys[0][SPRITE] = self.monkeys[0][ANIMATION][UP_STATE].next()
            self.monkeys[1][SPRITE] = self.monkeys[0][ANIMATION][DOWN_STATE].next()

        self.game.screen.blit(self.gfx_bg2, (-2 * (self.frame % 319), 0))
        self.game.screen.blit(self.gfx_bg1, (20, 0))
        self.game.screen.blit(self.monkeys[0][SPRITE], (self.game.GAME_WIDTH / 2 - 75, 100))

        # Overlay
        self.game.screen.blit(self.gfx_ladder, (self.game.GAME_WIDTH / 2 - 75, 100))
        self.game.screen.blit(self.gfx_ladder, (self.game.GAME_WIDTH / 2 + 75, 100))
        self.game.screen.blit(self.gfx_bg3, (-8 * (self.frame % 159), 0))
