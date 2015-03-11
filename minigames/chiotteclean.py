import pygame
from pygame.locals import *
import multiplayer
from input_map import *
import minigame
import input_map
from random import randint

class ChiotteGame(multiplayer.Minigame):

    name = "Clean this shit!"
    duration = 5
    balai = pygame.image.load('./res/img/chiotte_clean/balai.png')

    def __init__(self, game):
        minigame.Minigame.__init__(self, game)
        self.total_wipes = (self.difficulty + 1) * 8
        self.result = False
        self.width, self.height = self.screen.get_size()
        self.screen.fill((100,100,100))
        self.bowl = pygame.transform.scale(pygame.image.load('./res/img/chiotte_clean/bowl.png'), (self.width/2, self.height))
        self.balaipos = [self.height / 10 * 6, self.height / 10 * 6]
        p1turd_angle = randint(40, 160)
        p2turd_angle = randint(40, 160)
        self.fat_turd1 = pygame.transform.rotate(pygame.image.load('./res/img/chiotte_clean/fat_turd00.png'), p1turd_angle)
        self.fat_turd2 = pygame.transform.rotate(pygame.image.load('./res/img/chiotte_clean/fat_turd00.png'), p2turd_angle)
        self.med_turd1 = pygame.transform.rotate(pygame.image.load('./res/img/chiotte_clean/med_turd00.png'), p1turd_angle)
        self.med_turd2 = pygame.transform.rotate(pygame.image.load('./res/img/chiotte_clean/med_turd00.png'), p2turd_angle)
        self.low_turd1 = pygame.transform.rotate(pygame.image.load('./res/img/chiotte_clean/low_turd00.png'), p1turd_angle)
        self.low_turd2 = pygame.transform.rotate(pygame.image.load('./res/img/chiotte_clean/low_turd00.png'), p2turd_angle)
        self.no_turd = pygame.transform.rotate(pygame.image.load('./res/img/chiotte_clean/no_turd00.png'), 90)
        self.shits = [[self.fat_turd1, self.med_turd1, self.low_turd1, self.no_turd], [self.fat_turd2, self.med_turd2, self.low_turd2, self.no_turd]]
        self.p = [0, 0]
        self.wipes = [0, 0]
        self.curr_turd = [0, 0]
        self.player_won = [False, False]

    def draw(self):
        self.screen.blit(self.bowl, pygame.Rect(0, 0, self.width/2, self.height))
        self.screen.blit(self.bowl, pygame.Rect(self.width/2, 0, self.width/2, self.height))
        self.screen.blit(self.shits[0][self.curr_turd[0]], pygame.Rect(self.width/10 * 2, self.height/ 10 * 6, 40, 40))
        self.screen.blit(self.shits[1][self.curr_turd[1]], pygame.Rect(self.width / 10 * 7, self.height / 10 * 6, 40, 40))
        self.screen.blit(self.balai, pygame.Rect(self.width/10 * 2, self.balaipos[0], self.width/ 4, self.height / 4))
        self.screen.blit(self.balai, pygame.Rect(self.width/10 * 7, self.balaipos[1], self.width/ 4, self.height / 4))

    def tick(self):
        self.update()
        self.draw()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                for i in range(2):
                    if event.key == input_map.PLAYERS_MAPPING[i][input_map.UP]:
                        if self.p[i] >= -2:
                            self.p[i] -= 1
                            self.balaipos[i] -= 20
                            self.wipes[i] += 1
                            if self.wipes[i] < self.total_wipes and self.wipes[i] % (2 * (self.difficulty + 1)) == 0:
                                self.curr_turd[i] += 1
                    elif event.key == input_map.PLAYERS_MAPPING[i][input_map.DOWN]:
                        if self.p[i] <= 2:
                            self.p[i] += 1
                            self.balaipos[i] += 20
                            self.wipes[i] += 1
                            if self.wipes[i] < self.total_wipes and self.wipes[i] % (2 * (self.difficulty + 1)) == 0:
                                self.curr_turd[i] += 1
        if self.wipes[0] == self.total_wipes:
            self.player_won[0] = True
        if self.wipes[1] == self.total_wipes:
            self.player_won[1] = True

    def get_results(self):
        return self.player_won
