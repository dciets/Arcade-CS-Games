import pygame
from minigames import minigame


class LaddersMinigame(minigame.Minigame):
    name = "Evade the bees!"
    game_type = minigame.MULTIPLAYER
    max_duration = 50000

    BEE_BASE_SPEED = 10

    def __init__(self, game):
        minigame.Minigame.__init__(self, game)

        self.game = game

        self.bg1 = pygame.image.load("./res/img/ladders/bg1.png")
        self.bg2 = pygame.image.load("./res/img/ladders/bg2.png")
        self.bg3 = pygame.image.load("./res/img/ladders/bg3.png")
        self.ladder = pygame.image.load("./res/img/ladders/ladder.png")

    def init(self):
        pass

    def tick(self):
        self.game.screen.blit(self.bg2, (0, 0))
        self.game.screen.blit(self.bg1, (0, 0))
