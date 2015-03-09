from minigames import minigame
from minigames import multiplayer
from entities import PersoPlayer
from entities import PersoLeprechaun
from entities import Coin
import pygame
import input_map

class LeprechaunBeatemUp(multiplayer.Minigame):
    name = 'Hit the Leprechaun!'
    max_duration = 10000

    def __init__(self, game):
        minigame.Minigame.__init__(self, game)

        self.width = game.GAME_WIDTH
        self.height = game.GAME_HEIGHT

    def init(self):
        self.score = [0, 0]
        self.rainbow = pygame.image.load("./res/img/leprechaunBeatemUp/Background.png").convert()
        self.coin = pygame.image.load("./res/img/leprechaunBeatemUp/Coin.png").convert_alpha()

        self.players = [PersoPlayer(50, 300, "./res/img/leprechaunBeatemUp/Player1.png", self.difficulty), \
                        PersoPlayer(700, 300, "./res/img/leprechaunBeatemUp/Player2.png", self.difficulty), ]
        self.enemy = PersoLeprechaun(375, 300, "./res/img/leprechaunBeatemUp/Leprechaun.png", self.difficulty, self.players)
        self.coins = []
        self.currentTime = pygame.time.get_ticks()/1000.0

    def tick(self):
        self.score[0] = self.players[0].money
        self.score[1] = self.players[1].money

        self.events()
        self.update(pygame.time.get_ticks()/1000.0 - self.currentTime)
        self.draw()

        self.currentTime = pygame.time.get_ticks()/1000.0

    def get_results(self):
        if self.players[0].money > self.players[1].money:
            return [True, False]
        elif self.players[0].money < self.players[1].money:
            return [False, True]
        else:
            return [False, False]

    def update(self, timeElapsed):
        for player in self.players:
            player.update(timeElapsed)

        self.enemy.update(timeElapsed)

        for coin in self.coins:
            coin.update()

        for coin in self.coins:
            if coin.end():
                self.coins.remove(coin)

    def draw(self):
        self.screen.blit(self.rainbow, [0, 0])
        for player in self.players:
            player.draw(self.screen)

        self.enemy.draw(self.screen)

        for coin in self.coins:
            coin.draw(self.screen)

    def events(self):
        pygame.event.get()
        for i in range(2):
            keys = input_map.get_player_keys(i)
            if keys[input_map.UP]:
                self.players[i].move("up")
            if keys[input_map.RIGHT]:
                self.players[i].move("right")
            if keys[input_map.DOWN]:
                self.players[i].move("down")
            if keys[input_map.LEFT]:
                self.players[i].move("left")
            if keys[input_map.ACTION]:
                self.hit(i)

    def hit(self, player):
        if self.players[player].hit():
            if not self.enemy.isHurt() and self.players[player].sprite.rect.colliderect(self.enemy.sprite.rect):
                self.players[player].money += self.enemy.money
                self.enemy.hurt(self.players[player].pos)
                self.coins.append(Coin(self.players[player].pos))

            other = abs(player-1)
            if not self.players[other].isHurt() and self.players[player].sprite.rect.colliderect(self.players[other].sprite.rect):
                self.players[other].hurt(self.players[player].pos)
