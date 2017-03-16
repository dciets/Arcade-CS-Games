import pygame
from minigames import minigame
import input_map
import player 
import math
import multiplayer
import random


# Written and designed by Spencer Dube


class TreeBallz(minigame.Minigame):
    game_type = minigame.MULTIPLAYER
    name = 'Shoot the eyeball!!!'
    duration = 5
    playerImages = [pygame.image.load('./res/img/treeballz/Red.png'),pygame.image.load('./res/img/treeballz/RedF.png'),pygame.image.load('./res/img/treeballz/Blue.png'),pygame.image.load('./res/img/treeballz/BlueF.png')]
    projectileImages = [pygame.image.load('./res/img/treeballz/RedBullet.png'),pygame.image.load('./res/img/treeballz/BlueBullet.png')]
    board = pygame.image.load('./res/img/treeballz/Panel.png')
    ladders = [pygame.Rect(159,342,32,108),pygame.Rect(18,227,32,108),pygame.Rect(238,98,32,108),pygame.Rect(497,98,32,108),pygame.Rect(705,227,32,108),pygame.Rect(578,343,32,108)]
    platforms = [pygame.Rect(0,348,276,15),pygame.Rect(0,233,329,15),pygame.Rect(220,104,300,15),pygame.Rect(439,233,329,15),pygame.Rect(470,349,276,15)]
    def __init__(self, game):
        minigame.Minigame.__init__(self, game)
        self.width = game.GAME_WIDTH
        self.height = game.GAME_HEIGHT
        self.eyeballs = [
            pygame.Rect(random.randrange(50, 700),0, 32, 32),
            pygame.Rect(random.randrange(50, 700),0, 32, 32)
        ]
        self.lookingLeft = [False,False]
        self.projectiles = [[],[]]
        self.hits = [0,0]
        self.lastShot = [0.0,0.0]
        self.elapsedms = 0.0
        self.lastElapsed =0.0
        self.inLadder = [False,False]
        # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
        self.font = pygame.font.SysFont("monospace", 15)

    def tick(self):
        self.lastElapsed = self.elapsed_ms/1000.0
        self.elapsedms = pygame.time.get_ticks()/1000.0
        self.lastShot[0] += (self.elapsedms - self.lastElapsed)
        self.lastShot[1] += (self.elapsedms - self.lastElapsed)
        self.update()
        self.draw()

    def get_results(self):
        wins = [False,False]
        if self.hits[0] > self.hits[1]:
            wins[0] = True
        elif self.hits[0] < self.hits[1]:
            wins[1] = True
        return wins

    def draw(self):
        self.screen.blit(TreeBallz.board , [0,0])
        for i,eyeball in enumerate(self.eyeballs):
            if(i == 0 and self.lookingLeft[i] == True):
                self.screen.blit(TreeBallz.playerImages[1], eyeball)
            elif(i == 1 and self.lookingLeft[i] == True):
                self.screen.blit(TreeBallz.playerImages[3], eyeball)
            elif(i == 0):
                self.screen.blit(TreeBallz.playerImages[0], eyeball)
            else:
                self.screen.blit(TreeBallz.playerImages[2], eyeball)
        for i,list in enumerate(self.projectiles):
            for proj in list:
                self.screen.blit(TreeBallz.projectileImages[i],proj[0]['rect'])

        # render text
        p2Hits = self.font.render("Player 2 Hits: " + str(self.hits[1]), 1, (255,255,0))
        p1Hits = self.font.render("Player 1 Hits: " + str(self.hits[0]), 1, (255,255,0))
        self.screen.blit(p1Hits, (60, 10))
        self.screen.blit(p2Hits, (500, 10))

    def addProjectile(self,i,lookingLeft):
        self.projectiles[i].append([{'rect': pygame.Rect(self.eyeballs[i].x,self.eyeballs[i].y+5, 16, 16), 'leftFacing': lookingLeft}])

    def get_duration(self):
        return 10000

    def update(self):
        pygame.event.get()

        #Ladder Collision
        for i in range(2):
            ladderHits = 0
            for ladder in self.ladders:
                if self.eyeballs[i].colliderect(ladder):
                    self.inLadder[i] = True
                    ladderHits += 1
            if ladderHits == 0:
                self.inLadder[i] = False

        #Shitty gravity
        for i,eye in enumerate(self.eyeballs):
            onPlatform = False
            for platform in self.platforms:
                if eye.colliderect(platform) and not self.inLadder[i]:
                    eye.bottom = platform.top + 1 
                    onPlatform = True
            if eye.bottom < 480 and not self.inLadder[i] and not onPlatform:
                eye.y += 15
            elif eye.bottom > 480:
                eye.bottom = 480

        #Player movement and shooting
        for i in range(2):
            keys = input_map.get_player_keys(i)
            if len(keys) > 0:
                if keys[input_map.RIGHT]:
                    if self.eyeballs[i].right < 725:
                        self.eyeballs[i].x += 10
                        self.lookingLeft[i] = False
                if keys[input_map.LEFT]:
                    if self.eyeballs[i].left > 25:
                        self.eyeballs[i].x -= 10
                        self.lookingLeft[i] = True
                if keys[input_map.ACTION]:
                    if self.lastShot[i] > 80:
                        self.addProjectile(i,self.lookingLeft[i]);
                        self.lastShot[i] = 0.0
                if keys[input_map.UP] and self.inLadder[i]:
                        self.eyeballs[i].y -= 10
                if keys[input_map.DOWN] and self.inLadder[i]:
                        self.eyeballs[i].y += 10

        #TODO: Projectile movement.
        for i,list in enumerate(self.projectiles):
            for proj in list[:]:
                if proj[0]['leftFacing'] == True:
                    proj[0]['rect'].x -= 20
                else:
                    proj[0]['rect'].x += 20

                if i==0 and proj[0]['rect'].colliderect(self.eyeballs[1]):
                    self.hits[0] += 1
                    self.projectiles[i].remove(proj)
                elif i==1 and proj[0]['rect'].colliderect(self.eyeballs[0]):
                    self.hits[1] += 1
                    self.projectiles[i].remove(proj)