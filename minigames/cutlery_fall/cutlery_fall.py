from minigames import multiplayer
from Player import Player
from Cutlery import Cutlery
import pygame
import input_map
import random

class CutleryFall(multiplayer.Minigame):
    name = 'Press the right key!'
    max_duration = 10000

    def init(self):
        self.SPAWN_TIME = 1.0
        self.WAIT_TIME = 10
        self.DRAW_SPEED = 30
        self.currentTime = pygame.time.get_ticks()/1000.0 - self.SPAWN_TIME
        self.drawTime = pygame.time.get_ticks()/1000.0

        self.background = pygame.image.load("./res/img/cutleryFall/Background.png").convert()
        self.cutlery = pygame.image.load("./res/img/cutleryFall/knife.png").convert_alpha()

        self.players = [Player(), Player()]
        self.cutleries = []

    def run(self):
        self.tick()
        pygame.time.wait(self.WAIT_TIME)

    def tick(self):
        self.events()
        self.update()
        if pygame.time.get_ticks() - self.drawTime >= self.DRAW_SPEED:
            self.draw()
            self.drawTime = pygame.time.get_ticks()

    def get_results(self):
        if self.players[0].score > self.players[1].score:
            return [True, False]
        elif self.players[0].score < self.players[1].score:
            return [False, True]
        else:
            return [False, False]

    def update(self):
        for cutlery in self.cutleries:
            if cutlery.remove():
                self.cutleries.remove(cutlery)

        for cutlery in self.cutleries:
            cutlery.update()

        timeElapsed = pygame.time.get_ticks()/1000.0 - self.currentTime
        if timeElapsed >= self.SPAWN_TIME:
            self.cutleries.append(Cutlery(self.difficulty))
            self.currentTime = pygame.time.get_ticks()/1000.0

    def draw(self):
        # Draw screen
        self.screen.blit(self.background, [0, 0])
        for cutlery in self.cutleries:
            cutlery.draw(self.screen)

        # Draw info
        self.screen.blit(self.cutlery, (60,25))
        self.screen.blit(self.cutlery, (710,25))
        self.gfx.print_msg(str(self.players[0].score), (30, 30))
        self.gfx.print_msg(str(self.players[1].score), (750, 30))

        # Draw time
        elapsed_ms = pygame.time.get_ticks() - self.started_at
        duration = self.get_duration()
        sec_left = str(int((duration - elapsed_ms)/1000))
        self.gfx.print_msg(sec_left, (30, 550))

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                for cutlery in self.cutleries:
                    for i in range(2):
                        for j in range(len(input_map.PLAYERS_MAPPING[i])):
                            if event.key == input_map.PLAYERS_MAPPING[i][j] and cutlery.checkButton(j):
                                cutlery.slapped(i)
                                self.players[i].score += 1
