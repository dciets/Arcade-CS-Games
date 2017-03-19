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
    #Collection of enemy sprites, in this case 1 bat that is scaled and flipped to the right size and point in the right direction
    enemies = [pygame.transform.flip(pygame.transform.scale(pygame.image.load('./res/img/treeballz/bat.png'),[64,32]),True,False)]
    #Player image sprites
    playerImages = [pygame.image.load('./res/img/treeballz/Red.png'),pygame.image.load('./res/img/treeballz/RedF.png'),pygame.image.load('./res/img/treeballz/Blue.png'),pygame.image.load('./res/img/treeballz/BlueF.png')]
    #Player image sprites when damaged.
    playerImagesH = [pygame.image.load('./res/img/treeballz/RedP.png'),pygame.image.load('./res/img/treeballz/RedFP.png'),pygame.image.load('./res/img/treeballz/BlueP.png'),pygame.image.load('./res/img/treeballz/BlueFP.png')]
    #Projectile images, one for each player colour.
    projectileImages = [pygame.image.load('./res/img/treeballz/RedBullet.png'),pygame.image.load('./res/img/treeballz/BlueBullet.png')]
    #Board image.
    board = pygame.image.load('./res/img/treeballz/Panel.png')
    
    #Ladders and platform coordinates. Legacy hard coded.
    ladders = [pygame.Rect(159,342,32,108),pygame.Rect(18,227,32,108),pygame.Rect(238,98,32,108),pygame.Rect(497,98,32,108),pygame.Rect(705,227,32,108),pygame.Rect(578,343,32,108)]
    platforms = [pygame.Rect(0,348,276,15),pygame.Rect(0,233,329,15),pygame.Rect(220,104,300,15),pygame.Rect(439,233,329,15),pygame.Rect(470,349,276,15)]

    def __init__(self, game):
        minigame.Minigame.__init__(self, game)
        #Clock, screen width, screen height
        self.clock = pygame.time.Clock()
        self.width = game.GAME_WIDTH
        self.height = game.GAME_HEIGHT
        #Player rectangle data X is randomly selected for a spawn location
        self.eyeballs = [
            pygame.Rect(random.randrange(50, 700),0, 32, 32),
            pygame.Rect(random.randrange(50, 700),0, 32, 32)
        ]
        #Enemy rectangle data
        self.enemies = [
            pygame.Rect(0,0, 64, 32),
        ]
        #Bool indicating player is looking left
        self.lookingLeft = [False,False]
        #Colision with a bat, could be extended for multiple enemies to indicate hit invincibility
        self.batColliding = [False,False]
        #Projectile collections separated by player
        self.projectiles = [[],[]]
        #Hits (or score) for each player
        self.hits = [0,0]
        #Last shot time and hit timer indicating the time since last shooting and timer for hit indication
        self.lastShot = [0.0,0.0]
        self.hitTimer = [0.0,0.0]
        #Allows players to go up ladders at intersection
        self.inLadder = [False,False]
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
        #Decide who wins. More hits (points) more win.
        wins = [False,False]
        if self.hits[0] > self.hits[1]:
            wins[0] = True
        elif self.hits[0] < self.hits[1]:
            wins[1] = True
        return wins

    def draw(self):
        #Draw the board background
        self.screen.blit(TreeBallz.board , [0,0])
        
        #Draw the correct player sprite for which direction they're facing and whether they're damaged or not. Decrements the timer by 1 tick per rotation (~33ms)
        for i,eyeball in enumerate(self.eyeballs):
            if(i == 0 and self.lookingLeft[i] == True):
                if self.hitTimer[i] <= 0:
                    self.screen.blit(TreeBallz.playerImages[1], eyeball)
                    self.hitTimer[i] = 0
                else:
                    self.screen.blit(TreeBallz.playerImagesH[1], eyeball)
                    self.hitTimer[i] -= 33
            elif(i == 1 and self.lookingLeft[i] == True):
                if self.hitTimer[i] <= 0:
                    self.screen.blit(TreeBallz.playerImages[3], eyeball)
                    self.hitTimer[i] = 0
                else:
                    self.screen.blit(TreeBallz.playerImagesH[3], eyeball)
                    self.hitTimer[i] -= 33
            elif(i == 0):
                if self.hitTimer[i] <= 0:
                    self.screen.blit(TreeBallz.playerImages[0], eyeball)
                    self.hitTimer[i] = 0
                else:
                    self.screen.blit(TreeBallz.playerImagesH[0], eyeball)
                    self.hitTimer[i] -= 33
            else:
                if self.hitTimer[i] <= 0:
                    self.screen.blit(TreeBallz.playerImages[2], eyeball)
                    self.hitTimer[i] = 0
                else:
                    self.screen.blit(TreeBallz.playerImagesH[2], eyeball)
                    self.hitTimer[i] -= 33
        #Draw the projectiles
        for i,list in enumerate(self.projectiles):
            for proj in list:
                self.screen.blit(TreeBallz.projectileImages[i],proj[0]['rect'])
        #Draw the enemy
        for i,enemy in enumerate(self.enemies):
            self.screen.blit(TreeBallz.enemies[i],enemy)
        
        #Render text to show the hits
        p2Hits = self.font.render("Player 2 Hits: " + str(self.hits[1]), 1, (255,255,0))
        p1Hits = self.font.render("Player 1 Hits: " + str(self.hits[0]), 1, (255,255,0))
        self.screen.blit(p1Hits, (60, 10))
        self.screen.blit(p2Hits, (500, 10))

    def addProjectile(self,i,lookingLeft):
        #Adds a projectile going in the correct direction and assigns it to the right player
        self.projectiles[i].append([{'rect': pygame.Rect(self.eyeballs[i].x,self.eyeballs[i].y+5, 16, 16), 'leftFacing': lookingLeft}])

    def get_duration(self):
        #Set game time to 10 seconds
        return 10000

    def playerHit(self,player):
        #Hit player is marked
        self.hitTimer[player] += 330

        #Opposite player gets a point
        if player == 1:
            self.hits[0] += 1
        else:
            self.hits[1] += 1

    def sineUpdate(self):
        #Not quite a sine as it's absolute, more like bouncing.
        for enemi in self.enemies:
            #Increment X by 3 per tick, spend the rest of this function getting Y
            enemi.x += 3
            coeff = float(enemi.x)/float(self.width)
            enemi.y = abs(math.sin(coeff * math.pi * 4) * self.height * 0.9)
            #If the bat passes the end of the screen, reset the location.
            if enemi.x > self.width:
                enemi.x = 0

    def gravityUpdate(self):
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

    def playerUpdate(self):
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
                    if self.lastShot[i] > 0.25:
                        self.addProjectile(i,self.lookingLeft[i]);
                        self.lastShot[i] = 0.0
                if keys[input_map.UP] and self.inLadder[i]:
                        self.eyeballs[i].y -= 10
                if keys[input_map.DOWN] and self.inLadder[i]:
                        self.eyeballs[i].y += 10

    def ladderUpdate(self):
        #Ladder Collision
        for i in range(2):
            ladderHits = 0
            for ladder in self.ladders:
                if self.eyeballs[i].colliderect(ladder):
                    self.inLadder[i] = True
                    ladderHits += 1
            if ladderHits == 0:
                self.inLadder[i] = False

    def enemyCollision(self):
        #Enemy collision
        for i,enemi in enumerate(self.enemies):
            if enemi.colliderect(self.eyeballs[0]) and not self.batColliding[0]:
                self.batColliding[0] = True
                self.playerHit(0)
            elif not enemi.colliderect(self.eyeballs[0]):
                self.batColliding[0] = False
            if enemi.colliderect(self.eyeballs[1]) and not self.batColliding[1]:
                self.batColliding[1] = True
                self.playerHit(1)
            elif not enemi.colliderect(self.eyeballs[1]):
                self.batColliding[1] = False

    def projectileUpdate(self):
        #Projectile movement.
        for i,list in enumerate(self.projectiles):
            for proj in list[:]:
                if proj[0]['leftFacing'] == True:
                    proj[0]['rect'].x -= 20       
                else:
                    proj[0]['rect'].x += 20
                
                if proj[0]['rect'].x < 0 or proj[0]['rect'].x > 800:
                    self.projectiles[i].remove(proj)

                if i==0 and proj[0]['rect'].colliderect(self.eyeballs[1]):
                    self.playerHit(1)
                    self.projectiles[i].remove(proj)
                elif i==1 and proj[0]['rect'].colliderect(self.eyeballs[0]):
                    self.playerHit(0)
                    self.projectiles[i].remove(proj)

    def update(self):
        pygame.event.get()
        #Ladders
        self.ladderUpdate()
        #Enemies
        self.sineUpdate()
        #Gravity
        self.gravityUpdate()
        #Player location Update
        self.playerUpdate()
        #Enemy collision
        self.enemyCollision()
        #Projectile UPdate
        self.projectileUpdate()
