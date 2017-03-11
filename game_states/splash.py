import pygame
from pygame.locals import *
from datetime import datetime, timedelta
import random
from game_states.overlay_state import OverlayedState
import minigame
import endgame
import menu
import gfx

class Splash(OverlayedState):
    MINIGAMES = []

    '''Display the splash screen with some info in between minigames'''
    def __init__(self, game, results=[True, True]):
        OverlayedState.__init__(self, game)

        self.results = results
        self.started_at = datetime.now()
        self.screen = self.game.screen
        self.scrrct = self.screen.get_rect()

        print 'In Splash'
        print 'Difficulty:', self.game.difficulty
        print 'Type:', 'Multiplayer' if self.game.minigame.game_type == 2 else 'Singleplayer'
        print 'Lives', map(lambda p: p.lives, self.game.players)

    def run(self):
        pygame.event.clear()

        self.game.border.fill((0,0,0))
        self.display_hud()

        # Display minigame name
        self.game.gfx.print_msg(self.game.minigame.name, midtop=(self.scrrct.centerx, self.game.GAME_HEIGHT / 2), color=gfx.WHITE)

        # Display who's playing next for single player minigame
        if self.game.minigame.is_singleplayer():
            self.game.gfx.print_msg(self.game.players[self.game.active_player].university, midtop=(self.scrrct.centerx, self.scrrct.h - 100), color=gfx.RED if self.game.active_player == 0 else gfx.BLUE)

        if any(p.lives <= 0 for p in self.game.players) and not self.game.second_turn:
            self.game.state = endgame.EndGame(self.game, self.results)
        else:

            pygame.display.update()

            self.game.flash_outputs(self.results)

            pygame.time.delay(2000)

            self.game.state = minigame.Minigame(self.game)
