import inspect
import pygame
import sys
import random
import player
import minigames
from game_states import menu
import gfx

class Game:
    FPS = 30
    MINIGAMES = [g for _, g in inspect.getmembers(minigames, inspect.isclass)]

    def __init__(self, screen, font):
        '''Init game state, player score, game count, etc...'''
        self.screen = screen
        self.font = font
        self.gfx = gfx.Gfx(screen, font)
        self.state = menu.Menu(self)
        self.choose_minigame()
        self.difficulty = 0
        self.players = [player.Player(), player.Player()]
        self.active_player = 0
        self.second_turn = False

    def run(self):
        self.running = True
        while self.running:
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                sys.exit()
            self.state.run()
            pygame.display.update()

    def stop(self):
        self.running = False

    def choose_minigame(self):
        self.minigame = random.choice(Game.MINIGAMES)

