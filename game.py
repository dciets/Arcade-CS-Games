import inspect
import pygame
import sys
import random
from pygame.rect import Rect
from game_states.OverlayedState import OverlayedState
import player
import minigames
from game_states import menu
import gfx

class Game:
    FPS = 30
    MINIGAMES = [g for _, g in inspect.getmembers(minigames, inspect.isclass)]

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    BORDER_SIZE = 25
    GAME_WIDTH = SCREEN_WIDTH - 2 * BORDER_SIZE
    GAME_HEIGHT = SCREEN_HEIGHT - 2 * BORDER_SIZE
    GAME_TOP = BORDER_SIZE
    GAME_BOTTOM = SCREEN_HEIGHT - BORDER_SIZE
    GAME_LEFT = BORDER_SIZE
    GAME_RIGHT = SCREEN_HEIGHT - BORDER_SIZE

    def __init__(self, border, font):
        '''Init game state, player score, game count, etc...'''
        self.border = border
        self.screen = border.subsurface(Rect((Game.BORDER_SIZE, Game.BORDER_SIZE), (Game.SCREEN_WIDTH - 2 * Game.BORDER_SIZE, Game.SCREEN_HEIGHT - 2 * Game.BORDER_SIZE)))
        self.font = font
        self.gfx = gfx.Gfx(self.screen, font)
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

    def overlay(self):
        if isinstance(self.state, OverlayedState):
            self.states[-1].display_hud()


