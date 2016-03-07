import pygame
import input_map
from minigames import minigame
from minigames import multiplayer
from entities import Heart
from entities import PersoPlayer
from entities import Ring

class StayInTheRing(multiplayer.Minigame):
    name = 'Stay in the dome!'
    max_duration = 10000

    def __init__(self, game):
        minigame.Minigame.__init__(self, game)
        self.width = game.GAME_WIDTH
        self.height = game.GAME_HEIGHT

    def init(self):
        self.score = [0, 0]
        self.background = pygame.image.load("./res/img/stay_in_the_ring/Background.png").convert()
        self.ring = Ring(self.width/2, self.height/2, self.difficulty)
        self.players = [PersoPlayer(200, 450, "./res/img/stay_in_the_ring/Player1.png", self.difficulty), \
                        PersoPlayer(600, 450, "./res/img/stay_in_the_ring/Player2.png", self.difficulty), ]
        self.hearts = []
        self.currentTime = pygame.time.get_ticks()/1000.0

    def tick(self):
        self.score[0] = self.players[0].life
        self.score[1] = self.players[1].life

        self.events()
        self.update(pygame.time.get_ticks()/1000.0 - self.currentTime)
        self.draw()

        self.currentTime = pygame.time.get_ticks()/1000.0

    def get_results(self):
        if self.players[0].life > self.players[1].life:
            return [True, False]
        elif self.players[0].life < self.players[1].life:
            return [False, True]
        else:
            return [False, False]

    def update(self, timeElapsed):
        for player in self.players:
            player.update(timeElapsed)

        self.ring.update()
        self.dealOutsideRingDamage()
        self.checkEndGame()

        for heart in self.hearts:
            heart.update()

        for heart in self.hearts:
            if heart.end():
                self.hearts.remove(heart)

    def draw(self):
        self.screen.blit(self.background, [0, 0])
        for player in self.players:
            player.draw(self.screen)

        self.ring.draw(self.screen)

        for heart in self.hearts:
            heart.draw(self.screen)

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
            other = abs(player-1)
            if self.players[player].sprite.rect.colliderect(self.players[other].sprite.rect):
                self.players[other].recoil(self.players[player].pos)

    def dealOutsideRingDamage(self):
        for player in self.players:
            if not player.isHurt() and not player.sprite.rect.colliderect(self.ring.collisionBox):
                player.hurt()
                self.hearts.append(Heart(player.pos))

    def checkEndGame(self):
        for player in self.players:
            if player.life == 0:
                self.elapsed_ms = 10000