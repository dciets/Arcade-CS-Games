import inspect
import pygame
import sys
import random
from pygame.rect import Rect
from game_states.overlay_state import OverlayedState
import player
import minigames
from game_states import menu
import gfx


def cycle_shuffled_iterator(items):
    '''
    Iterates infinitely through shuffled versions of the given list
    '''
    xs = items[:]
    i = len(xs)

    while True:
        if i == len(xs):
            random.shuffle(xs)
            i = 0

        yield xs[i]

        i += 1


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

    def __init__(self, border, font, outputs):
        '''Init game state, player score, game count, etc...'''
        self.border = border
        self.screen = border.subsurface(Rect((Game.BORDER_SIZE, Game.BORDER_SIZE), (Game.SCREEN_WIDTH - 2 * Game.BORDER_SIZE, Game.SCREEN_HEIGHT - 2 * Game.BORDER_SIZE)))
        self.font = font
        self.gfx = gfx.Gfx(self.screen, font)
        self.triggers = [True, True]
        self.state = menu.Menu(self)
        self.outputs = outputs
        self.init()

    def init(self):
        self.game_iterator = cycle_shuffled_iterator(Game.MINIGAMES)
        self.choose_minigame()
        self.difficulty = 0
        self.players = [player.Player(), player.Player()]
        self.active_player = 0
        self.second_turn = False

    def run(self):
        self.running = True
        while self.running:
            if pygame.key.get_pressed()[pygame.K_q]:
                sys.exit()

            self.state.run()
            pygame.display.update()


    def stop(self):
        self.running = False

    def choose_minigame(self):
        self.minigame = next(self.game_iterator)

    def overlay(self):
        if isinstance(self.state, OverlayedState):
            self.states[-1].display_hud()

    def flash_outputs(self, results):
        self.outputs.state[0] = (not results[0]) and self.triggers[0]
        self.outputs.state[1] = (not results[1]) and self.triggers[1]
        self.outputs.write()

        pygame.time.delay(1000)

        self.outputs.state[0] = False
        self.outputs.state[1] = False
        self.outputs.write()
