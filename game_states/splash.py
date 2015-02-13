import pygame
from pygame.locals import *
from datetime import datetime, timedelta
import random
import minigame
import endgame
import gfx

HEART_SPRITE = pygame.image.load('res/img/heart.png')

class Splash:
    MINIGAMES = []
    _duration = 3

    '''Display the splash screen with some info in between minigames'''
    def __init__(self, game):
        self.game = game
        self.started_at = datetime.now()
        self.screen = self.game.screen
        self.scrrct = self.screen.get_rect()

        print 'In Splash'
        print 'Difficulty:', self.game.difficulty
        print 'Type:', 'Multiplayer' if self.game.minigame.game_type == 2 else 'Singleplayer'
        print 'Lives', map(lambda p: p.lives, self.game.players)

    def run(self):
        if(self.started_at + timedelta(seconds=self._duration) < datetime.now()):
            self.game.state = minigame.Minigame(self.game)

        if any(p.lives <= 0 for p in self.game.players) and not self.game.second_turn:
            self.game.state = endgame.EndGame(self.game)

        self.screen.fill((0,0,0))

        # Display minigame name
        self.game.gfx.print_msg(self.game.minigame.name, midtop=(self.scrrct.centerx, 300), color=gfx.WHITE)

        # Display players lives
        self.game.gfx.print_msg("Player 1", topleft=(30, 30), color=gfx.RED)
        self.game.gfx.print_msg("Player 2", topright=(self.scrrct.w-30, 30), color=gfx.RED)

        heart_rect = HEART_SPRITE.get_rect()
        heart_rect.topleft = (30, 70)
        for i in range(self.game.players[0].lives):
            self.game.screen.blit(HEART_SPRITE, heart_rect.move(i*(heart_rect.w+10), 0))

        heart_rect.topright = (self.game.screen.get_rect().w - 30, 70)
        for i in range(self.game.players[1].lives):
            self.game.screen.blit(HEART_SPRITE, heart_rect.move(-i*(heart_rect.w+10), 0))

        # Display who's playing next for single player minigame
        if self.game.minigame.is_singleplayer():
            self.game.gfx.print_msg("Player {}".format(self.game.active_player+1), midtop=(self.scrrct.centerx, self.scrrct.h - 100), color=gfx.BLUE)
