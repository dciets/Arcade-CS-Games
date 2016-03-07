from itertools import cycle, islice, tee, dropwhile
import pygame
from pygame.locals import *
import random
import re
import operator
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
        self.font = pygame.font.Font('res/font/ps2p.ttf', 14)
        self.schools_scores = json.load(open('./res/schools_scores.json', 'r'))
        self.schools = cycle(list(enumerate(sorted(self.schools_scores.keys(), key=lambda k: random.random()))))
        s1, s2 = tee(self.schools)
        [s1.next() for i in range(random.randint(0, len(self.schools_scores.keys())))]
        [s2.next() for i in range(random.randint(0, len(self.schools_scores.keys())))]
        self.selectors = [s1, s2]
        self.selections = [
            self.selectors[0].next(),
            self.selectors[1].next()
        ]
        self.players_is_ready = [False, False]

        # Gfx
        self.gfx_background = pygame.image.load('./res/img/ui/background.jpg')
        self.gfx_header = pygame.image.load('./res/img/ui/header.png').convert_alpha()
        self.gfx_grid = pygame.image.load('./res/img/ui/menu.png').convert_alpha()
        self.gfx_vs = pygame.image.load('./res/img/ui/vs.png').convert_alpha()
        self.gfx_selections = [self.selections[0][1], self.selections[1][1]]
        self.gfx_selectors = [
            pygame.image.load('./res/img/ui/p1_selector.png').convert_alpha(),
            pygame.image.load('./res/img/ui/p2_selector.png').convert_alpha()
        ]



        # Text
        self.txt_repo = pygame.font.Font('res/font/ps2p.ttf', 11).render("github.com/dciets/Arcade-CS-Games", 0, (255, 255, 255))
        self.txt_ready = [pygame.font.Font('res/font/ps2p.ttf', 13).render("Ready!", 0, (255, 0, 0)), pygame.font.Font('res/font/ps2p.ttf', 13).render("Ready!", 0, (0, 0, 255))]
        self.txt_not_ready = [pygame.font.Font('res/font/ps2p.ttf', 13).render("Ready!", 0, (0, 0, 0)), pygame.font.Font('res/font/ps2p.ttf', 13).render("Ready!", 0, (0, 0, 0))]

        ''' BLITTING '''
        # Background
        self.game.border.blit(self.gfx_background, (0, 0))
        self.game.border.blit(self.gfx_header, (-5, 0))

        # Player infos
        self.update_selection(0)
        self.update_selection(1)
        self.game.border.blit(self.gfx_vs, self.gfx_vs.get_rect(topleft=(125, 200)))

        # High scores
        self.show_top10()

        # Link to repository
        self.game.border.blit(self.txt_repo, self.txt_repo.get_rect(bottomright=(self.game.SCREEN_WIDTH - 5, self.game.SCREEN_HEIGHT - 2)))

    def show_player_list(self):
        # Position school iterator
        while self.schools.next()[0] != len(self.schools_scores.keys()) - 1: pass

        # Player list
        for i in range(len(self.schools_scores.keys())):
            start_x = self.game.SCREEN_WIDTH - 410
            start_y = self.game.SCREEN_HEIGHT - 522
            gfx_school = pygame.image.load('./res/img/ui/' + re.sub(r'\W+', '', self.schools.next()[1].lower()) + '.png').convert_alpha()
            self.game.border.blit(gfx_school, gfx_school.get_rect(topleft=(start_x + (i % 4) * 99, start_y + (i / 4) * 100)))
        self.game.border.blit(self.gfx_grid, self.gfx_grid.get_rect(bottomright=(self.game.SCREEN_WIDTH - 5, self.game.SCREEN_HEIGHT - 15)))

    def update_selection(self, idx):
        txt_score = pygame.font.Font('res/font/ps2p.ttf', 13).render(str(self.schools_scores[self.selections[idx][1]]), 0, (255, 255, 255))
        txt_score_hide = pygame.font.Font('res/font/ps2p.ttf', 13).render("000000", 0, (0, 0, 0))
        start_x = self.game.SCREEN_WIDTH - 410
        start_y = self.game.SCREEN_HEIGHT - 522

        self.show_player_list()

        self.gfx_selections[idx] = pygame.image.load('./res/img/ui/' + re.sub(r'\W+', '', self.selections[idx][1].lower()) + '.png').convert_alpha()
        self.game.border.blit(self.gfx_selections[idx], self.gfx_selections[idx].get_rect(topleft=(idx * 230 + 30, 210)))
        pygame.draw.rect(self.game.border, (0, 0, 0), txt_score_hide.get_rect(midtop=(idx * 230 + 70, 300)))
        self.game.border.blit(txt_score, txt_score.get_rect(midtop=(idx * 230 + 70, 300)))
        self.game.border.blit(self.gfx_selectors[0], self.gfx_selectors[0].get_rect(topleft=(start_x + (self.selections[0][0] % 4) * 99, start_y + (self.selections[0][0] / 4) * 100)))
        self.game.border.blit(self.gfx_selectors[1], self.gfx_selectors[1].get_rect(topleft=(start_x + (self.selections[1][0] % 4) * 99, start_y + (self.selections[1][0] / 4) * 100)))

    def show_top10(self):
        i = 1
        for school in list(sorted(self.schools_scores.iteritems(), key=operator.itemgetter(1), reverse=True)[:10]):
            entry = pygame.font.Font('res/font/ps2p.ttf', 12).render("#" + str(i) + " " + str(school[0]) + " - " + str(school[1]), 0, (255, 255, 255))
            self.game.border.blit(entry, entry.get_rect(topleft=(50, 350 + (i - 1) * 20)))
            i += 1

    def run(self):
        if self.players_is_ready[0] and self.players_is_ready[1]:
            pygame.time.wait(1000)
            self.start_game()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                for i in range(2):
                    if event.key == input_map.PLAYERS_MAPPING[i][input_map.DOWN] and not self.players_is_ready[i]:
                        while self.selectors[i].next()[0] != (self.selections[i][0] + 3) % len(self.schools_scores.keys()): pass
                        self.selections[i] = self.selectors[i].next()
                        self.update_selection(i)
                    elif event.key == input_map.PLAYERS_MAPPING[i][input_map.UP] and not self.players_is_ready[i]:
                        while self.selectors[i].next()[0] != (self.selections[i][0] - 5) % len(self.schools_scores.keys()): pass
                        self.selections[i] = self.selectors[i].next()
                        self.update_selection(i)
                    elif event.key == input_map.PLAYERS_MAPPING[i][input_map.RIGHT] and not self.players_is_ready[i]:
                        while self.selectors[i].next()[0] != (((self.selections[i][0] - (self.selections[i][0] / 4) * 4 + 1) % 4 - 1) + (self.selections[i][0] / 4) * 4) % len(self.schools_scores.keys()): pass
                        self.selections[i] = self.selectors[i].next()
                        self.update_selection(i)
                    elif event.key == input_map.PLAYERS_MAPPING[i][input_map.LEFT] and not self.players_is_ready[i]:
                        # Screw maths and iterators for this one
                        col = self.selections[i][0] - (self.selections[i][0] / 4) * 4
                        if col == 0:
                            while self.selectors[i].next()[0] != self.selections[i][0] + 2: pass
                        else:
                            while self.selectors[i].next()[0] != (self.selections[i][0] - 2) % len(self.schools_scores.keys()): pass
                        self.selections[i] = self.selectors[i].next()
                        self.update_selection(i)

                    if event.key == input_map.PLAYERS_MAPPING[i][input_map.ACTION]:
                        self.players_is_ready[i] = not self.players_is_ready[i]

                        if self.players_is_ready[i]:
                            self.game.border.blit(self.txt_ready[i], self.txt_ready[i].get_rect(topleft=(i * 230 + 40, 190)))
                        else:
                            self.game.border.blit(self.txt_not_ready[i], self.txt_not_ready[i].get_rect(topleft=(i * 230 + 40, 190)))

    def start_game(self):
        self.game.players[0].university = self.selections[0][1]
        self.game.players[1].university = self.selections[1][1]
        self.game.state = splash.Splash(self.game)
