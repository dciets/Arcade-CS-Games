from itertools import cycle
import pygame
import random
from math import sin, pi
from pygame.constants import KEYDOWN, KEYUP
from pygame.rect import Rect
from input_map import PLAYERS_MAPPING, UP, DOWN
from minigames import minigame

SPRITE = 0
ANIMATION = 1

STILL_STATE = 0
UP_STATE = 1
DOWN_STATE = 2

BEE_BASE_SPEED = 10
BEE_SPAWN_RATE = 14

class LaddersMinigame(minigame.Minigame):
    name = "Dodge the bees!"
    game_type = minigame.MULTIPLAYER
    max_duration = 10000

    def __init__(self, game):
        minigame.Minigame.__init__(self, game)

        self.game = game
        self.positions = [
            (self.game.GAME_WIDTH / 2 - 75, random.randint(100, 440)),
            (self.game.GAME_WIDTH / 2 + 75, random.randint(100, 440))
        ]
        self.bee_speed = BEE_BASE_SPEED * max(1, (self.difficulty / 2.0))
        self.bee_spawn_rate = max(BEE_SPAWN_RATE - 2 * self.difficulty, 6)

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
        self.monkey_states = [STILL_STATE, STILL_STATE]

    def init(self):
        self.results = [True, True]
        self.monkeys = [
            [self.gfx_monkeys[0][STILL_STATE].next(), self.gfx_monkeys[0]],
            [self.gfx_monkeys[1][STILL_STATE].next(), self.gfx_monkeys[1]]
        ]

    def tick(self):
        # Check collisions
        for i in range(2):
            for j in range(len(self.bees[i])):
                for k in range(2):
                    if self.results[k]:
                            if self.bees[i][j][SPRITE].get_rect(topleft=self.bees[i][j][2]).colliderect(self.monkeys[k][SPRITE].get_rect(topleft=self.positions[k])):
                                self.results[k] = False
                                self.monkey_states[i] = STILL_STATE

        # Process events
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                for i in range(2):
                    if event.key == PLAYERS_MAPPING[i][UP] and self.results[i]:
                        self.monkey_states[i] = UP_STATE
                    elif event.key == PLAYERS_MAPPING[i][DOWN] and self.results[i]:
                        self.monkey_states[i] = DOWN_STATE
            elif event.type == KEYUP :
                for i in range(2):
                    if event.key == PLAYERS_MAPPING[i][UP] or event.key == PLAYERS_MAPPING[i][DOWN]:
                        self.monkey_states[i] = STILL_STATE

        # Spawn bees
        if self.frame % self.bee_spawn_rate == 0:
            if len(self.bees[0]) >= len(self.bees[1]):
                self.bees[1].append([self.gfx_bees[1].next(), self.gfx_bees[1], (800, random.randint(100, 440))])
            elif len(self.bees[1]) > len(self.bees[0]):
                self.bees[0].append([self.gfx_bees[0].next(), self.gfx_bees[0], (0, random.randint(100, 440))])

        # Move bees
        for i in range(2):
            for j in range(len(self.bees[i])):
                if i == 0:
                    self.bees[i][j][2] = (self.bees[i][j][2][0] + self.bee_speed, self.bees[i][j][2][1])
                elif i == 1:
                    self.bees[i][j][2] = (self.bees[i][j][2][0] - self.bee_speed, self.bees[i][j][2][1])

        # Move monkeys
        for i in range(2):
            if self.results[i]:
                if self.monkey_states[i] == UP_STATE:
                    self.positions[i] = (self.positions[i][0], max(self.positions[i][1] - 5, 100))
                elif self.monkey_states[i] == DOWN_STATE:
                    self.positions[i] = (self.positions[i][0], min(self.positions[i][1] + 5, 440))

                if self.frame % 2 == 0:
                    self.monkeys[i][SPRITE] = self.monkeys[i][ANIMATION][self.monkey_states[i]].next()
                    for j in range(len(self.bees[i])):
                        self.bees[i][j][SPRITE] = self.bees[i][j][ANIMATION].next()
            else:
                self.positions[i] = (self.positions[i][0], self.positions[i][1] + 10)

        # Background
        self.game.screen.blit(self.gfx_bg2, (-2 * (self.frame % 319), 0))
        self.game.screen.blit(self.gfx_bg1, (20, 0))

        # Entities
        self.game.screen.blit(self.monkeys[0][SPRITE], self.positions[0])
        self.game.screen.blit(self.monkeys[1][SPRITE], self.positions[1])
        for i in range(2):
            for bee in self.bees[i]:
                self.game.screen.blit(bee[SPRITE], bee[2])

        # Overlay
        self.game.screen.blit(self.gfx_ladder, (self.game.GAME_WIDTH / 2 - 75, 100))
        self.game.screen.blit(self.gfx_ladder, (self.game.GAME_WIDTH / 2 + 75, 100))
        self.game.screen.blit(self.gfx_bg3, (-8 * (self.frame % 159), 0))

    def get_results(self):
        return self.results