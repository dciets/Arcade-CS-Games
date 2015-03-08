import pygame
from pygame.locals import *
import splash
import json
import input_map

class Menu:
    '''
    Display the initial menu waiting for play to get ready
    and pick universities.
    '''
    def __init__(self, game):
        self.game = game
        self.schools_scores = json.load(open('./res/schools_scores.json', 'r'))
        self.font = pygame.font.Font('res/font/ps2p.ttf', 14)
        self.player1_txt = self.font.render("<Choose your school>", 0, (255, 0, 0))
        self.player1_label = self.player1_txt.get_rect()
        self.player1_label.topleft = (200 - self.player1_label.width/2, 20)

        self.vs_txt = game.font.render("VS", 0, (255, 255, 255))
        self.vs_label = self.vs_txt.get_rect()
        self.vs_label.topleft = (game.GAME_WIDTH / 2 - self.vs_label.width/2, 10)

        self.player2_txt = self.font.render("<Choose your school>", 0, (0, 0, 255))
        self.player2_label = self.player2_txt.get_rect()
        self.player2_label.topleft = (game.GAME_HEIGHT - self.player2_label.width/2, 20)

        self.players_selection = [[0, 0], [0, 0]]
        self.selected = [False, False]

    def run(self):
        # Show game menu
        # Perhaps something that await two player input
        # while display "Insert coins..."
        self.game.border.fill((0, 0, 0))

        r = pygame.Rect(self.players_selection[0][0]*175 + 10, 65 + self.players_selection[0][1]*100, 180, 80)
        pygame.draw.rect(self.game.screen, (255, 0, 0), r, not self.selected[0])
        r = pygame.Rect(self.players_selection[1][0]*175 + 20, 75 + self.players_selection[1][1]*100, 160, 60)
        pygame.draw.rect(self.game.screen, (0, 0, 255), r, not self.selected[1])

        if self.selected[0]:
            school = self.schools_scores.keys()[self.players_selection[0][0]*5 + self.players_selection[0][1]]
            school_name = self.font.render(school, 0, (255, 0, 0))
            self.game.screen.blit(school_name, Rect(self.player1_label.x + self.player1_label.width/2 - school_name.get_rect().width/2, self.player1_label.y, self.player1_label.width, self.player1_label.height))
        else:
            self.game.screen.blit(self.player1_txt, self.player1_label)
        self.game.screen.blit(self.vs_txt, self.vs_label)
        if self.selected[1]:
            school = self.schools_scores.keys()[self.players_selection[1][0]*5 + self.players_selection[1][1]]
            school_name = self.font.render(school, 0, (0, 0, 255))
            self.game.screen.blit(school_name, Rect(self.player2_label.x + self.player2_label.width/2 - school_name.get_rect().width/2, self.player2_label.y, self.player2_label.width, self.player2_label.height))
        else:
            self.game.screen.blit(self.player2_txt, self.player2_label)

        i = 0
        for key in self.schools_scores.keys():
            school_name = self.font.render(key, 0, (255, 255, 255))
            school_score = self.font.render(str(self.schools_scores[key]), 0, (255, 255, 255))
            school_rect = school_name.get_rect()
            school_rect.topleft = (int(i/5)*175 + 100, 100 + (i % 5)*100)
            school_rect.x -= school_rect.width/2
            school_rect.y -= school_rect.height/2
            self.game.screen.blit(school_name, school_rect)
            self.game.screen.blit(school_score, Rect(school_rect.x + school_rect.width/2 - school_score.get_rect().width/2, school_rect.y+20, school_rect.width, school_rect.height))
            i += 1

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                for i in range(2):
                    if not self.selected[i]:
                        if event.key == input_map.PLAYERS_MAPPING[i][input_map.DOWN]:
                            self.players_selection[i][1] += 1
                            if self.players_selection[i][1] > 4:
                                self.players_selection[i][1] = 0
                        elif event.key == input_map.PLAYERS_MAPPING[i][input_map.UP]:
                            self.players_selection[i][1] -= 1
                            if self.players_selection[i][1] < 0:
                                self.players_selection[i][1] = 4
                        elif event.key == input_map.PLAYERS_MAPPING[i][input_map.RIGHT]:
                            self.players_selection[i][0] += 1
                            if self.players_selection[i][0] > 3:
                                self.players_selection[i][0] = 0
                        elif event.key == input_map.PLAYERS_MAPPING[i][input_map.LEFT]:
                            self.players_selection[i][0] -= 1
                            if self.players_selection[i][0] < 0:
                                self.players_selection[i][0] = 3
                    if event.key == input_map.PLAYERS_MAPPING[i][input_map.ACTION]:
                        self.selected[i] = not self.selected[i]
                        if self.selected[0] and self.selected[1]:
                            self.start_game()

    def start_game(self):
        school_player1 = self.schools_scores.keys()[self.players_selection[0][0]*5 + self.players_selection[0][1]]
        school_player2 = self.schools_scores.keys()[self.players_selection[1][0]*5 + self.players_selection[1][1]]
        self.game.players[0].university = school_player1
        self.game.players[1].university = school_player2
        self.game.state = splash.Splash(self.game)

