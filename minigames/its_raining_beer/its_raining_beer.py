from minigames import multiplayer
import pygame
from player import Player
from beer_manager import BeerManager
import input_map


class ItsRainingBeer(multiplayer.Minigame):
    name = 'Drink beer!'
    max_duration = 10000
    MAX_BEERS = 10

    def init(self):
        self.width, self.height = self.screen.get_size()
        background = pygame.image.load("res/img/its_raining_beer/background.png")
        background = pygame.transform.scale(background, (self.width, self.height))
        self.background = background.convert()
        self.game_rect = pygame.Rect(0, 0, self.width, int(self.height * 0.78))
        self.players = [Player("p1", (int(0.25 * self.width), int(self.height * 0.78)), int(0.05 * self.width)),
                        Player("p2", (int(0.75 * self.width), int(self.height * 0.78)), int(0.05 * self.width))]
        self.beer_manager = BeerManager(self.MAX_BEERS, 6 + self.difficulty * 2, (self.width, self.height))

    def tick(self):
        self.beer_manager.update()

        pygame.event.get()
        for i, player in enumerate(self.players):
            keys = input_map.get_player_keys(i)
            direction = 0

            if keys[input_map.ACTION]:
                player.jump()

            if keys[input_map.RIGHT]:
                direction = 1
            elif keys[input_map.LEFT]:
                direction = -1
            player.move(direction, self.game_rect, [p for p in self.players if p != player][0])
            self.beer_manager.detect_collision(player)

        self.screen.blit(self.background, [0, 0])
        for player in self.players:
            player.blit(self.screen)
        self.beer_manager.blit(self.screen)

        self.score = [self.players[0].score, self.players[1].score]

    def get_results(self):
        if self.players[0].score == 0 and self.players[1].score == 0:
            return [False, False]
        elif self.players[0].score > self.players[1].score:
            return [True, False]
        elif self.players[0].score < self.players[1].score:
            return [False, True]
        else:
            return [True, True]
