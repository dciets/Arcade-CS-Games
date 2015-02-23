from datetime import datetime, timedelta
import pygame
import splash

class Minigame:
    '''Play a minigame!'''
    def __init__(self, game):
        self.game = game
        self.minigame = self.game.minigame(self.game)
        self.duration = self.minigame.get_duration()
        self.started_at = pygame.time.get_ticks()

        self.minigame.init()

        print('In minigame!')

    def run(self):
        self.minigame.run()

        if (self.started_at + self.duration) < pygame.time.get_ticks():
            self.game_done()

    def game_done(self):
        results = self.minigame.get_results()
        for player, result in zip(self.game.players, results):
            if not result:
                player.lives -= 1
        self.game.state = splash.Splash(self.game)

        if any(results):
            self.game.difficulty += 1

        if self.game.minigame.is_singleplayer():
            self.game.active_player = 1 - self.game.active_player
            self.game.second_turn = not self.game.second_turn

