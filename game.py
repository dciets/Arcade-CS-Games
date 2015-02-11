import sys
import random
import player
from minigames import *
from game_states import menu

class Game:
    MINIGAMES = [STest, MTest]

    def __init__(self):
        '''Init game state, player score, game count, etc...'''
        self.state = menu.Menu(self)
        self.minigame = random.choice(Game.MINIGAMES)
        self.difficulty = 0
        self.players = [player.Player(), player.Player()]

    def run(self):
        self.running = True
        while self.running:
            self.state.run()

    def stop(self):
        self.running = False

