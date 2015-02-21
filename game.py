import inspect
import pygame
import sys
import random
import player
import minigames
from game_states import menu
import gfx

class Game:
    #MINIGAMES = [g for _, g in inspect.getmembers(minigames, inspect.isclass)]
    MINIGAMES = [minigames.BlackCat]

    def __init__(self, screen, font):
        '''Init game state, player score, game count, etc...'''
        self.screen = screen
        self.font = font
        self.gfx = gfx.Gfx(screen, font)
        self.state = menu.Menu(self)
        self.minigame = random.choice(Game.MINIGAMES)
        self.difficulty = 0
        self.players = [player.Player(), player.Player()]
        self.active_player = 0
        self.second_turn = False

    def run(self):
        self.running = True
        while self.running:
            self.state.run()
            pygame.display.update()

    def stop(self):
        self.running = False

