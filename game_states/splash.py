import pygame
from pygame.locals import *
from datetime import datetime, timedelta
import random
import minigame
import endgame

class Splash:
    MINIGAMES = []
    _duration = 3

    '''Display the splash screen with some info in between minigames'''
    def __init__(self, game):
        self.game = game
        self.started_at = datetime.now()

        self.gamename = game.font.render(self.game.minigame.name, 0, (255,255,255))
        self.gamename_rect = self.gamename.get_rect()
        self.gamename_rect.topleft = (50, 300)

        print 'In Splash'
        print 'Difficulty:', self.game.difficulty
        print 'Type:', 'Multiplayer' if self.game.minigame.game_type == 2 else 'Singleplayer'
        print 'Lives', map(lambda p: p.lives, self.game.players)

    def run(self):
        if(self.started_at + timedelta(seconds=self._duration) < datetime.now()):
            self.game.state = minigame.Minigame(self.game)

        if any(p.lives <= 0 for p in self.game.players):
            self.game.state = endgame.EndGame(self.game)

        self.game.screen.fill((0,0,0))
        self.game.screen.blit(self.gamename, self.gamename_rect)
