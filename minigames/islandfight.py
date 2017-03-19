import pygame
from minigames import minigame
import input_map
import player
import math
import multiplayer
import random


# Designed by Lenon and SuperFatBob
# Code and "Art" by SuperFatBob


class IslandFight(minigame.Minigame):
    game_type = minigame.MULTIPLAYER
    name = 'Island Fight!!!'
    playerImages = [pygame.image.load('./res/img/islandFight/Red.png'),pygame.image.load('./res/img/islandFight/Blue.png')]
    projectileImages = [pygame.image.load('./res/img/islandFight/RedBullet.png'),pygame.image.load('./res/img/islandFight/BlueBullet.png')]
    islandImage = pygame.image.load('./res/img/islandFight/island.png')
    pushBack = 40
    projectileSpeed = 20
    moveSpeed = 10
    waterSpeed = 1
    playerDead = 2

    def __init__(self, game):
        minigame.Minigame.__init__(self, game)
        self.clock = pygame.time.Clock()
        self.width = game.GAME_WIDTH
        self.height = game.GAME_HEIGHT
        self.players = [
            pygame.Rect(150,150, 32, 32),
            pygame.Rect(550,350, 32, 32)
        ]
        self.waters = [
            pygame.Rect(0,0, 800, 50),
            pygame.Rect(0,0, 50, 600),
            pygame.Rect(0,500, 800, 50),
            pygame.Rect(700,0, 50, 600)
        ]
        self.looking = [1,3]
        self.projectiles = [[],[]]
        self.lastShot = [0.0,0.0]
        self.elapsedms = 0.0
        self.lastElapsed =0.0
        # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
        self.font = pygame.font.SysFont("monospace", 15)

    def tick(self):
        #Clock tick at 33ms
        self.clock.tick(33)
        #Increase last shot by the tick to limit shot speed of players
        equElapsed = self.clock.get_time()/1000.0
        self.lastShot=[x+equElapsed for x in self.lastShot]
        #Update then draw the view.
        self.update()
        self.draw()

    def get_results(self):
        if self.playerDead == 0:
            wins = [False,True]
        elif self.playerDead == 1:
            wins = [True,False]
        else:
            wins = [False,False]
        return wins

    def draw(self):
        self.screen.blit(self.islandImage , [50,50])
        for i, plr in enumerate(self.players):
            self.screen.blit(self.playerImages[i], plr)
        for i, projectile in enumerate(self.projectiles):
            for proj in projectile:
                self.screen.blit(self.projectileImages[i],proj[0]['rect'])

        self.waters[0] = pygame.draw.rect(self.screen, pygame.Color(0, 0, 255), self.waters[0], 0)
        self.waters[1] = pygame.draw.rect(self.screen, pygame.Color(0, 0, 255), self.waters[1], 0)
        self.waters[2] = pygame.draw.rect(self.screen, pygame.Color(0, 0, 255), self.waters[2], 0)
        self.waters[3] = pygame.draw.rect(self.screen, pygame.Color(0, 0, 255), self.waters[3], 0)

    def addProjectile(self,i,looking):
        self.projectiles[i].append([{'rect': pygame.Rect(self.players[i].x,self.players[i].y+5, 16, 16), 'direction': looking}])

    def get_duration(self):
        return 10000

    def update(self):
        pygame.event.get()

        #Player movement and shooting
        for i in range(2):
            keys = input_map.get_player_keys(i)
            if len(keys) > 0:
                if keys[input_map.RIGHT]:
                    self.players[i].x += self.moveSpeed
                    self.looking[i] = 1
                if keys[input_map.LEFT]:
                    self.players[i].x -= self.moveSpeed
                    self.looking[i] = 3
                if keys[input_map.ACTION]:
                    if self.lastShot[i] > 0.2:
                        self.addProjectile(i,self.looking[i]);
                        self.lastShot[i] = 0.0
                if keys[input_map.UP]:
                    self.players[i].y -= self.moveSpeed
                    self.looking[i] = 0
                if keys[input_map.DOWN]:
                    self.players[i].y += self.moveSpeed
                    self.looking[i] = 2

        for i,list in enumerate(self.projectiles):
            for proj in list[:]:
                if proj[0]['direction'] == 0:
                    proj[0]['rect'].y -= self.projectileSpeed
                elif proj[0]['direction'] == 1:
                    proj[0]['rect'].x += self.projectileSpeed
                elif proj[0]['direction'] == 2:
                    proj[0]['rect'].y += self.projectileSpeed
                else:
                    proj[0]['rect'].x -= self.projectileSpeed

                if i==0 and proj[0]['rect'].colliderect(self.players[1]):
                    if proj[0]['direction'] == 0:
                        self.players[1].y -= self.pushBack
                    elif proj[0]['direction'] == 1:
                        self.players[1].x += self.pushBack
                    elif proj[0]['direction'] == 2:
                        self.players[1].y += self.pushBack
                    else:
                        self.players[1].x -= self.pushBack
                    self.projectiles[i].remove(proj)

                elif i==1 and proj[0]['rect'].colliderect(self.players[0]):
                    if proj[0]['direction'] == 0:
                        self.players[0].y -= self.pushBack
                    elif proj[0]['direction'] == 1:
                        self.players[0].x += self.pushBack
                    elif proj[0]['direction'] == 2:
                        self.players[0].y += self.pushBack
                    else:
                        self.players[0].x -= self.pushBack
                    self.projectiles[i].remove(proj)

        for i,water in enumerate(self.waters):
            if water.colliderect(self.players[0]):
                self.playerDead = 0
                self.game.state.game_done()
            elif water.colliderect(self.players[1]):
                self.playerDead = 1
                self.game.state.game_done()

        if random.randint(0,1) == 0:
            self.waters[0].height += self.waterSpeed
        else:
            self.waters[1].width += self.waterSpeed

        if random.randint(0, 1) == 0:
            self.waters[2].height += self.waterSpeed
            self.waters[2].y -= self.waterSpeed
        else:
            self.waters[3].width += self.waterSpeed
            self.waters[3].x -= self.waterSpeed

