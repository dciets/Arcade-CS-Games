from itertools import cycle, islice, tee, dropwhile
import pygame
from pygame.locals import *
from pygame.transform import rotozoom
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
        self.schools = sorted(self.schools_scores.keys())
        self.selections = [
            random.randint(0, len(self.schools) - 1),
            random.randint(0, len(self.schools) - 1)
        ]

        self.players_is_ready = [False, False]

        # Gfx
        self.gfx_background = pygame.image.load('./res/img/ui/background.jpg')
        self.gfx_grid = pygame.image.load('./res/img/ui/menu.png').convert_alpha()
        self.gfx_vs = pygame.image.load('./res/img/ui/vs.png').convert_alpha()

        # Text
        self.txt_repo = pygame.font.Font('res/font/ps2p.ttf', 11).render("github.com/dciets/Arcade-CS-Games", 0, (255, 255, 255))
        self.txt_ready = [pygame.font.Font('res/font/ps2p.ttf', 42).render("READY", 0, (255, 255, 255)), pygame.font.Font('res/font/ps2p.ttf', 42).render("READY", 0, (255, 255, 255))]
        for i in range(2):
            self.txt_ready[i] = rotozoom(self.txt_ready[i], 35.0, 1.0)
        self.txt_wet_mode = [pygame.font.Font('res/font/ps2p.ttf', 20).render("< Wet mode! >", 0, (255, 255, 0)), pygame.font.Font('res/font/ps2p.ttf', 20).render("< Wet mode! >", 0, (255, 255, 0))]
        self.txt_dry_mode = [pygame.font.Font('res/font/ps2p.ttf', 20).render("< Dry mode! >", 0, (255, 255, 0)), pygame.font.Font('res/font/ps2p.ttf', 20).render("< Dry mode! >", 0, (255, 255, 0))]

        self.team_font = pygame.font.Font('res/font/ps2p.ttf', 30)
        self.txt_teams = [None, None]
        self.colors = [(0xff, 0x26, 0x47), (0x00, 0xea, 0xcc)]
        self.refresh_team(0)
        self.refresh_team(1)

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

    def update_selection(self, index):
        x = self.game.SCREEN_WIDTH/2 * index + self.game.SCREEN_WIDTH/4
        y = self.game.SCREEN_HEIGHT * 0.75
        fill = self.colors[index]

        self.arrow(x, y + 50, True, fill, width=50, linewidth=7, height=10)
        self.arrow(x, y - 50, False, fill, width=50, linewidth=7, height=10)

        self.game.border.blit(self.txt_teams[index], self.txt_teams[index].get_rect(center=(x, y)))

        if self.players_is_ready[index]:
            self.game.border.blit(self.txt_ready[index], self.txt_ready[index].get_rect(center=(x, y)))

        if self.game.triggers[index]:
            self.game.border.blit(self.txt_wet_mode[index], self.txt_wet_mode[index].get_rect(center=(x, y - 100)))
        else:
            self.game.border.blit(self.txt_dry_mode[index], self.txt_dry_mode[index].get_rect(center=(x, y - 100)))

    def show_top10(self):
        i = 1
        for school in list(sorted(self.schools_scores.iteritems(), key=operator.itemgetter(1), reverse=True)[:10]):
            entry = pygame.font.Font('res/font/ps2p.ttf', 15).render("#" + str(i) + " " + str(school[0]) + " - " + str(school[1]), 0, (255, 255, 255))
            self.game.border.blit(entry, entry.get_rect(topleft=(800/2 + 50, 50 + (i - 1) * 20)))
            i += 1


    def refresh_team(self, index):
        self.txt_teams[index] = self.team_font.render(self.schools[self.selections[index]], 0, self.colors[index])


    def handle_player_input(self, index, event):
        if not self.players_is_ready[index]:
            if event.key == input_map.PLAYERS_MAPPING[index][input_map.UP]:
                self.selections[index] = (self.selections[index] - 1) % len(self.schools)
                self.refresh_team(index)

            elif event.key == input_map.PLAYERS_MAPPING[index][input_map.DOWN]:
                self.selections[index] = (self.selections[index] + 1) % len(self.schools)
                self.refresh_team(index)

            if event.key == input_map.PLAYERS_MAPPING[index][input_map.RIGHT] or event.key == input_map.PLAYERS_MAPPING[index][input_map.LEFT]:
                self.game.triggers[index] = not self.game.triggers[index]

        if event.key == input_map.PLAYERS_MAPPING[index][input_map.ACTION]:
            self.players_is_ready[index] = not self.players_is_ready[index]

    def arrow(self, x, y, down, color, width=50, height=25, linewidth=5):
        f = down and 1 or -1
        points = [[x - width / 2, y - (height / 2) * f],
                  [x, y + (height / 2) * f],
                  [x + width / 2, y - (height / 2) * f]]

        pygame.draw.lines(self.game.border, color, False, points, linewidth)

    def run(self):
        # Background
        self.game.border.blit(self.gfx_background, (0, 0))

        self.game.border.blit(self.txt_repo, self.txt_repo.get_rect(bottomright=(self.game.SCREEN_WIDTH - 5, self.game.SCREEN_HEIGHT - 2)))

        self.show_top10()

        for i in range(2):
            self.update_selection(i)

        if self.players_is_ready[0] and self.players_is_ready[1]:
            pygame.display.update()
            pygame.time.wait(1000)
            self.start_game()
            return

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                for i in range(2):
                    self.handle_player_input(i, event)


    def start_game(self):
        for i, player in enumerate(self.game.players):
            player.university = self.schools[self.selections[i]]

        self.game.state = splash.Splash(self.game)
