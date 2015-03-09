import pygame
from minigames import minigame
from input_map import *
from player import Player
from position_patterns import generate_targets


class ShootTargets(minigame.Minigame):

    name = 'Shoot the targets!'
    game_type = minigame.MULTIPLAYER

    def __init__(self, game):
        minigame.Minigame.__init__(self, game)

        self.screen_rect = self.screen.get_rect()
        self.score = [0, 0]
        self.sprites = []
        self.players = [Player(self, 0), Player(self, 1)]
        self.targets = generate_targets(self)

    def get_results(self):
        return [self.players[0].points >= self.players[1].points,
                self.players[0].points <= self.players[1].points]

    def tick(self):
        self.score[0] = self.players[0].points
        self.score[1] = self.players[1].points

        keys = pygame.key.get_pressed()

        for i, player in enumerate(self.players):
            player.flare = False

            if keys[PLAYERS_MAPPING[i][LEFT]]:
                player.direction[0] = -1
            elif keys[PLAYERS_MAPPING[i][RIGHT]]:
                player.direction[0] = 1
            else:
                player.direction[0] = 0

            if keys[PLAYERS_MAPPING[i][UP]]:
                player.direction[1] = -1
            elif keys[PLAYERS_MAPPING[i][DOWN]]:
                player.direction[1] = 1
            else:
                player.direction[1] = 0

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                for i, player in enumerate(self.players):
                    if event.key == PLAYERS_MAPPING[i][ACTION]:
                        player.flare = True

        entities = self.targets + self.players + self.sprites

        for entity in entities:
            entity.update()

        self.targets = filter(lambda t: not t.hit, self.targets)
        self.sprites = filter(lambda s: not s.finished, self.sprites)

        self.screen.fill((20, 23, 32))

        for entity in entities:
            entity.render()