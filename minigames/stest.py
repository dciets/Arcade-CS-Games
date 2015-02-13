import pygame
from pygame.locals import *
import singleplayer

class STest(singleplayer.Singleplayer):
    name = "Singleplayer Test"

    def init(self):
        self.result = False

    def tick(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_w:
                    self.result = True
                elif event.key == K_l:
                    self.result = False

        self.gfx.print_msg("[W]in or [L]ose", (50, 50))

        if self.result:
            self.gfx.print_msg("Winning", (50, 100), color=(0, 255, 0))
        else:
            self.gfx.print_msg("Losing", (50, 100), color=(255, 0, 0))

    def get_result(self):
        return self.result
