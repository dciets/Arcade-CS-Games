from minigames import multiplayer
from Player import Player
from Cutlery import Cutlery
from people import People
import pygame
import input_map
import math

class CutleryFall(multiplayer.Minigame):
    name = 'Press the right key!'
    max_duration = 10000

    def init(self):
        self.NB_PLAYERS = 2
        self.PEOPLE_DISTANCE = 100
        self.SPAWN_TIME = 0.5
        self.currentTime = pygame.time.get_ticks()/1000.0 - self.SPAWN_TIME
        self.spawn = 0.0

        self.background = pygame.image.load("./res/img/cutleryFall/Background.png").convert()

        self.players = [Player(), Player()]
        self.cutleries = []
        self.visits = []

    def tick(self):
        self.events()
        self.update()
        self.draw()

    def get_results(self):
        if self.players[0].score > self.players[1].score:
            return [True, False]
        elif self.players[0].score < self.players[1].score:
            return [False, True]
        else:
            return [False, False]

    def update(self):
        timeElapsed = pygame.time.get_ticks()/1000.0 - self.currentTime
        self.currentTime = pygame.time.get_ticks()/1000.0
        
        for player in self.players:
            player.update(timeElapsed)
        
        for cutlery in self.cutleries:
            if cutlery.destroy:
                self.cutleries.remove(cutlery)

        for cutlery in self.cutleries:
            cutlery.update()
            if not cutlery.active and cutlery.visit:
                pos = self.PEOPLE_DISTANCE * math.ceil(len(self.visits) / 2)
                if len(self.visits) % 2 == 0:
                    pos = -pos
                self.visits.append(People(cutlery.cutleryType, pos))
                cutlery.visit = False

        self.spawn += timeElapsed
        if self.spawn >= self.SPAWN_TIME:
            self.cutleries.append(Cutlery(self.difficulty))
            self.spawn = 0.0

    def draw(self):
        # Draw screen
        self.screen.blit(self.background, [0, 0])
        for visit in self.visits:
            visit.draw(self.screen)
        for cutlery in self.cutleries:
            cutlery.draw(self.screen)

        # Draw info
        self.gfx.print_msg(str(self.players[0].score), (30, 30))
        self.gfx.print_msg(str(self.players[1].score), (750, 30))

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                for i in range(self.NB_PLAYERS):
                    if not self.players[i].freeze:
                        for j in range(len(input_map.PLAYERS_MAPPING[i])):
                            if event.key == input_map.PLAYERS_MAPPING[i][j]:
                                self.players[i].freeze = True
                                for cutlery in self.cutleries:
                                    if cutlery.checkButton(j):
                                        cutlery.slapped(i)
                                        self.players[i].score += 1
                                        self.players[i].freeze = False
                                        break
                                
                                i = self.NB_PLAYERS - 1
                                j = len(input_map.PLAYERS_MAPPING[i]) - 1
