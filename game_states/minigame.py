from datetime import datetime, timedelta
import pygame
from pygame.constants import USEREVENT
from pygame.time import Clock
from game_states.OverlayedState import OverlayedState
import splash

class Minigame(OverlayedState):
    '''Play a minigame!'''
    def __init__(self, game):
        OverlayedState.__init__(self, game)

        self.game = game
        self.minigame = self.game.minigame(self.game)
        self.elapsed_ms = 0
        self.duration = self.minigame.get_duration()
        self.timer = Clock()
        self.minigame.init()

        print('In minigame!')

    def run(self):
        self.game.border.fill((0,0,0))
        self.minigame.run()
        self.display_hud()
        self.elapsed_ms += self.timer.tick(self.game.FPS)

        if int(self.minigame.sec_left) <= 0:
            self.game_done()

    def game_done(self):
        results = self.minigame.get_results()
        for player, result in zip(self.game.players, results):
            if not result:
                player.lives -= 1
        self.game.state = splash.Splash(self.game)

        if self.game.minigame.is_singleplayer():
            if self.game.second_turn:
                self.game.difficulty += 1
                self.game.choose_minigame()
            self.game.active_player = 1 - self.game.active_player
            self.game.second_turn = not self.game.second_turn
        else:
            self.game.difficulty += 1
            self.game.choose_minigame()

