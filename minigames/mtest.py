import pygame
from pygame.locals import *
import minigame

class MTest(minigame.Minigame):
    name = "Multiplayer Test"
    game_type = minigame.MULTIPLAYER

    def init(self):
        self.result = False

    def tick(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_w:
                    self.result = True
                elif event.key == K_l:
                    self.result = False

        self.print_msg("[W]in or [L]ose", (50, 50))

        if self.result:
            self.print_msg("Winning", (50, 100), (0, 255, 0))
        else:
            self.print_msg("Losing", (50, 100), (255, 0, 0))

    def get_results(self):
        return [self.result, self.result]
