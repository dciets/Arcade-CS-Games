import pygame
from pygame.locals import *
import singleplayer
from input_map import *

class STest(singleplayer.Minigame):
    name = "Singleplayer Test"

    def init(self):
        self.result = False

    def tick(self):
        pygame.event.get()
        self.result = self.get_player_keys()[UP]

        self.gfx.print_msg("[W]in or [L]ose", (50, 50))

        if self.result:
            self.gfx.print_msg("Winning", (50, 100), color=(0, 255, 0))
        else:
            self.gfx.print_msg("Losing", (50, 100), color=(255, 0, 0))

    def get_result(self):
        return self.result
