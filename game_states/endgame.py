#-*-encoding=utf-8-*-
from datetime import datetime, timedelta
import json
import pygame
import menu


class EndGame:
    '''Display end game score'''
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font('res/font/ps2p.ttf', 22)
        self.started_at = datetime.now()
        self.winner = -1
        f = open('./res/schools_scores.json', 'r')
        self.schools_scores = json.load(f)
        for i in range(2):
            if self.game.players[i].lives > 0:
                self.winner = i
        self.player_points = []
        for player in self.game.players:
            points = (self.game.difficulty - (3-player.lives)) * 100
            if points <= 0:
                points = 0
            self.player_points.append(points)
            self.schools_scores[player.university] += points
        f = open('./res/schools_scores.json', 'w')
        f.write(json.dumps(self.schools_scores))
        print('In end game screen')

    def run(self):
        self.game.border.fill((0,0,0))

        pygame.event.clear()

        if self.winner == -1:
            win_txt = self.font.render('It\'s a draw !', 0, (255, 255, 255))
        else:
            win_txt = self.font.render('The winner is : ' + self.game.players[self.winner].university +'!', 0, (255, 255, 255))
        win_rect = win_txt.get_rect()
        win_rect.topleft = (50, 50)
        self.game.screen.blit(win_txt, win_rect)

        for i in range(2):
            txt = self.game.players[i].university + " gained " + str(self.player_points[i]) + " points"
            txt2 = 'New score : ' + str(self.schools_scores[self.game.players[i].university])
            pts = self.font.render(txt, 0, (255, 0, 0) if i == 0 else (0, 0, 255))
            pts_rect = pts.get_rect()
            pts_rect.topleft = (50, 100*(i+1))
            new_score = self.font.render(txt2, 0, (255, 0, 0) if i == 0 else (0, 0, 255))
            new_score_rect = new_score.get_rect()
            new_score_rect.topleft = (50, 100*(i+1) + 50)
            self.game.screen.blit(pts, pts_rect)
            self.game.screen.blit(new_score, new_score_rect)

        if self.started_at + timedelta(seconds=10) < datetime.now():
            self.game.init()
            self.game.state = menu.Menu(self.game)

