import pygame
from minigames import minigame
from input_map import *
from player import Player
import math

class Rope(minigame.Minigame):
    name = 'Jump over the rope'
    game_type = minigame.MULTIPLAYER

    def __init__(self, game):
        minigame.Minigame.__init__(self, game)
        self.amplitude = 100
        self.screen_rect = self.screen.get_rect().size
        self.players = [Player(self, 0), Player(self, 1)]
        self.rate = 1


    def get_results(self):
        return [self.players[0].points >= self.players[1].points,
                self.players[0].points <= self.players[1].points]

    
    def tick(self):
        resolution = 10
        dx = float(self.screen_rect[0]) / resolution

        x = [i * dx for i in range(resolution + 1)]
        y = [self.screen_rect[1] / 2 + self.y(xi, self.elapsed_ms / 1000.0) for xi in x]

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                for i, player in enumerate(self.players):
                    if event.key == PLAYERS_MAPPING[i][ACTION]:
                        player.jump()

        for player in self.players:
            player.update()

        self.screen.fill((135, 206, 235))

        ground = self.screen_rect[1] / 2 + self.amplitude - 5
        pygame.draw.rect(self.screen, (0, 92, 9), (0, ground, self.screen_rect[0], self.screen_rect[1] / 2))

        # Players in the back of the rope
        for player in self.players:
            if not self.in_front(self.players[0].x - 25):
                player.render()

        pygame.draw.lines(self.screen, (255, 235, 198), False, zip(map(int, x), map(int, y)), 5)

        # Players in the front of the rope
        for player in self.players:
            if self.in_front(self.players[0].x - 25):
                player.render()


    def y(self, x, t):
        return self.amplitude * math.sin(math.pi *  x / float(self.screen_rect[0])) * math.cos(2 * self.rate * math.pi * t + math.pi)

    def in_front(self, x):
        t = self.elapsed_ms / 1000.0
        return math.sin(2 * self.rate * math.pi * t + math.pi) > 0

    def hittest(self):
        t = self.elapsed_ms / 1000.0
        y = (math.sin(2 * self.rate * math.pi * t + math.pi))
        d = -2 * math.pi * self.rate * math.cos(2 * math.pi * self.rate * t + math.pi)

        return abs(y) < 0.25 and d < 0
