import pygame
from pygame.locals import *
from datetime import datetime, timedelta
import random
from game_states.OverlayedState import OverlayedState
import minigame
import endgame
import gfx

class Splash(OverlayedState):
    MINIGAMES = []
    _duration = 3

    '''Display the splash screen with some info in between minigames'''
    def __init__(self, game):
        OverlayedState.__init__(self, game)

        self.started_at = datetime.now()
        self.screen = self.game.screen
        self.scrrct = self.screen.get_rect()

        print 'In Splash'
        print 'Difficulty:', self.game.difficulty
        print 'Type:', 'Multiplayer' if self.game.minigame.game_type == 2 else 'Singleplayer'
        print 'Lives', map(lambda p: p.lives, self.game.players)

    def run(self):
        pygame.event.clear()

        if(self.started_at + timedelta(seconds=self._duration) < datetime.now()):
            self.game.state = minigame.Minigame(self.game)

        if any(p.lives <= 0 for p in self.game.players) and not self.game.second_turn:
            self.game.state = endgame.EndGame(self.game)

        self.game.border.fill((0,0,0))
        self.display_hud()

        # Display minigame name
        self.game.gfx.print_msg(self.game.minigame.name, midtop=(self.scrrct.centerx, self.game.GAME_HEIGHT / 2), color=gfx.WHITE)

        # Display who's playing next for single player minigame
        if self.game.minigame.is_singleplayer():
            self.game.gfx.print_msg(self.game.players[self.game.active_player].university, midtop=(self.scrrct.centerx, self.scrrct.h - 100), color=gfx.RED if self.game.active_player == 0 else gfx.BLUE)
