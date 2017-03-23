import pygame
from minigames import minigame
import input_map
import player 
import math
import multiplayer
import random

#Created by David Sylvestre (cocoatchannel)

class HotPotato(minigame.Minigame):
    game_type = minigame.MULTIPLAYER
    name = "PASS THE BOMB!!"
    MIN_DURATION = 10
    MAX_DURATION = 25
    MIN_CONTROLS_SEQUENCE = 3
    MAX_CONTROLS_SEQUENCE = 5
    BOMB_DIMENSIONS = 200
    CONTROL_DIMENSION = 80
    CONTROLS_COUNT = 5
    
    #Load images   
    bombImage = pygame.image.load('./res/img/hotpotato/bomb.png')
    explosionImage = pygame.image.load('./res/img/hotpotato/explosion.png')
    arrowImage = pygame.image.load('./res/img/hotpotato/Arrow.png')
    buttonImage = pygame.image.load('./res/img/hotpotato/Button.png')
    keyFrameImage = pygame.image.load('./res/img/hotpotato/KeyFrame.png')
    keyFramePressedImage = pygame.image.load('./res/img/hotpotato/KeyFramePressed.png')
    leftHand = pygame.image.load('./res/img/hotpotato/LeftHand.png')
    rightHand = pygame.image.load('./res/img/hotpotato/RightHand.png')
    
    #Initialize control sprites
    controlsSprites = [
             arrowImage, pygame.transform.rotate(arrowImage, -90), pygame.transform.rotate(arrowImage, -180), pygame.transform.rotate(arrowImage, -270), buttonImage,
    ]
    
    #inputMap = [input_map.UP, input_map.LEFT, input_map.DOWN, input_map.RIGHT, input_map.ACTION]
    
    
    def __init__(self, game):
        minigame.Minigame.__init__(self, game)
        self.width = game.GAME_WIDTH
        self.height = game.GAME_HEIGHT
        
        self.textFont = pygame.font.Font('res/font/ps2p.ttf', 18)
        
        self.bombExploded = False
        self.duration = random.randint(self.MIN_DURATION, self.MAX_DURATION) * 1000 #random explosion time
        self.bombPlayerIndex = random.randint(0, 1) #Who has the bomb
        self.generateControlSequence()
        
        bombScale = 0.37
        w,h = self.bombImage.get_size()
        self.bombImage = pygame.transform.scale(self.bombImage, (int(w*bombScale), int(h*bombScale))) #Too lazy to resize he image
        self.BOMB_DIMENSIONS = self.BOMB_DIMENSIONS * bombScale
        self.bombPositions = [
                [103 - 17, 190 + self.BOMB_DIMENSIONS + 69], 
                [self.width - (318 - 34) + 103, 140 + self.BOMB_DIMENSIONS + 144]
        ]
        
        w,h = self.explosionImage.get_size()
        self.explosionImage = pygame.transform.scale(self.explosionImage, (int(w*bombScale), int(h*bombScale))) #Too lazy to resize he image
        
        
        
        #Clears the event buffer
        pygame.event.get()

        
    def tick(self):
        self.update()
        self.draw()
        return

        
    def get_results(self):
        wins = [True,True]
        wins[self.bombPlayerIndex] = False
        return wins

        
    def passBomb(self):
        self.bombPlayerIndex = (self.bombPlayerIndex + 1) % 2
    
    
    def generateControlSequence(self):
        self.controlToPress = 0
        self.controlSequence = []
        self.controlPositions = []
        self.nbOfControlsInSequence = random.randint(self.MIN_CONTROLS_SEQUENCE, self.MAX_CONTROLS_SEQUENCE)
        initialOffset = (self.width - (self.CONTROL_DIMENSION * self.nbOfControlsInSequence)) / 2
        
        for i in range(self.nbOfControlsInSequence):
            self.controlSequence.append(random.randint(0, self.CONTROLS_COUNT - 1))
            self.controlPositions.append([initialOffset + (self.CONTROL_DIMENSION * i), 30])
            
            
        text = ("Left" if self.bombPlayerIndex == 0  else "Right") + " has the bomb!"
        text_width, text_height = self.textFont.size(text)
        self.textWidth = text_width
        self.label = self.textFont.render(text, 0, (255, 255, 255))
        
    
    def get_duration(self):
        if not self.bombExploded:
            return 20000 + self.elapsed_ms #doesn't show when the game will really end
        else:
            return self.duration 
        
        
    def draw(self):
        self.screen.blit(self.leftHand, [0, 300])
        self.screen.blit(self.rightHand, [self.width - 175, 300])
        
        if not self.bombExploded:
            self.screen.blit(self.bombImage, self.bombPositions[self.bombPlayerIndex])
        else:
            self.screen.blit(self.explosionImage, self.bombPositions[self.bombPlayerIndex])
        
        for i in range(self.nbOfControlsInSequence):
            self.screen.blit(self.keyFramePressedImage if self.controlToPress > i else self.keyFrameImage, self.controlPositions[i])
            self.screen.blit(self.controlsSprites[self.controlSequence[i]], self.controlPositions[i])
        
        
        self.screen.blit(self.label, [(self.width / 2) - (self.textWidth / 2), self.CONTROL_DIMENSION + 30 + 40])
        

            
    def update(self):
        if not self.bombExploded and self.elapsed_ms >= self.duration:
            self.bombExploded = True
            self.duration = 3000 + self.elapsed_ms #The game ends 3 seconds after the bomb exploded
        
        
        if not self.bombExploded:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == input_map.PLAYERS_MAPPING[self.bombPlayerIndex][self.controlSequence[self.controlToPress]]: #Good key to press for current player
                        self.controlToPress = self.controlToPress + 1 #Next key to press
                        if self.controlToPress == len(self.controlSequence): #The player finished the sequence
                            self.passBomb()
                            self.generateControlSequence()
                            break #prevents multiple keys to be correctly input in the same frame
                    else:
                        self.controlToPress = 0