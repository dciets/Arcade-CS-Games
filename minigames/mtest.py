import pygame
from pygame.locals import *
import multiplayer
from input_map import *

class MTest(multiplayer.Minigame):
    name = "Multiplayer Test"

    def init(self):
        self.results = [False, False]

    def tick(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                for i in range(2):
                    if event.key == PLAYERS_MAPPING[i][UP]:
                        self.results[i] = True
                    elif event.key == PLAYERS_MAPPING[i][DOWN]:
                        self.results[i] = False

        self.gfx.print_msg("[W]in or [L]ose", (50, 50))

        if self.results[0]:
            self.gfx.print_msg("Winning", (50, 100), color=(0, 255, 0))
        else:
            self.gfx.print_msg("Losing", (50, 100), color=(255, 0, 0))

        if self.results[1]:
            self.gfx.print_msg("Winning", topright=(750, 100), color=(0, 255, 0))
        else:
            self.gfx.print_msg("Losing", topright=(750, 100), color=(255, 0, 0))

    def get_results(self):
        return self.results
