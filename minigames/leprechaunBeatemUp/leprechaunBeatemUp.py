from minigames import multiplayer
from entities import PersoPlayer
from entities import PersoLeprechaun
from entities import Coin
import pygame
import input_map

class LeprechaunBeatemUp(multiplayer.Minigame):
    name = 'Hit the Leprechaun!'
    max_duration = 10000

    def init(self):
        self.WAIT_TIME = 10
        self.DRAW_SPEED = 30

        self.width, self.height = self.screen.get_size()

        self.rainbow = pygame.image.load("./res/img/leprechaunBeatemUp/Background.png").convert()
        self.coin = pygame.image.load("./res/img/leprechaunBeatemUp/Coin.png").convert_alpha()

        self.players = [PersoPlayer(50, 300, "./res/img/leprechaunBeatemUp/Player1.png", self.difficulty), \
                        PersoPlayer(750, 300, "./res/img/leprechaunBeatemUp/Player2.png", self.difficulty), ]
        self.enemy = PersoLeprechaun(400, 300, "./res/img/leprechaunBeatemUp/Leprechaun.png", self.difficulty, self.players)
        self.coins = []
        self.currentTime = pygame.time.get_ticks()/1000.0
        self.drawTime = pygame.time.get_ticks()/1000.0

    def run(self):
        self.tick()
        pygame.time.wait(self.WAIT_TIME)

    def tick(self):
        timeElapsed = pygame.time.get_ticks()/1000.0 - self.currentTime
        self.currentTime = pygame.time.get_ticks()/1000.0

        self.events()
        self.update(timeElapsed)
        if pygame.time.get_ticks() - self.drawTime >= self.DRAW_SPEED:
            self.draw()
            self.drawTime = pygame.time.get_ticks()

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

        self.screen.blit(self.coin, (60,25))
        self.screen.blit(self.coin, (710,25))
        self.gfx.print_msg(str(self.players[0].money), (30, 30))
        self.gfx.print_msg(str(self.players[1].money), (750, 30))

        elapsed_ms = pygame.time.get_ticks() - self.started_at
        duration = self.get_duration()

        sec_left = str(int((duration - elapsed_ms)/1000))
        self.gfx.print_msg(sec_left, (30, 550))

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
