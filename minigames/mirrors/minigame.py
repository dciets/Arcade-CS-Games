import os
import random
import operator
import pygame
from pygame.locals import *
from input_map import *
from minigames import multiplayer


class Mirrors(multiplayer.Minigame):
    name = "Break The Mirrors!"


    def init(self):
        self.mirror_images = [ os.path.join("minigames/mirrors/images", f) for f in os.listdir("minigames/mirrors/images") if f.startswith("mirror") and os.path.isfile(os.path.join("minigames/mirrors/images", f)) ]
        self.results = [False, False]

    def tick(self):
        mirror_img_raw = pygame.image.load(random.choice(self.mirror_images))
        mirror_img = pygame.transform.scale(mirror_img_raw, map(operator.mul, mirror_img_raw.get_size(), len(mirror_img_raw.get_size()) * (5,)))
        mirror_rect = mirror_img.get_rect()
        self.screen.blit(mirror_img, mirror_rect)
        pygame.display.flip()
        






        # for event in pygame.event.get():
        #     if event.type == KEYDOWN:
        #         for i in range(2):
        #             if event.key == PLAYERS_MAPPING[i][UP]:
        #                 self.results[i] = True
        #             elif event.key == PLAYERS_MAPPING[i][DOWN]:
        #                 self.results[i] = False
        #
        # self.gfx.print_msg("[W]in or [L]ose", (50, 50))
        #
        # if self.results[0]:
        #     self.gfx.print_msg("Winning", (50, 100), color=(0, 255, 0))
        # else:
        #     self.gfx.print_msg("Losing", (50, 100), color=(255, 0, 0))
        #
        # if self.results[1]:
        #     self.gfx.print_msg("Winning", topright=(750, 100), color=(0, 255, 0))
        # else:
        #     self.gfx.print_msg("Losing", topright=(750, 100), color=(255, 0, 0))

    def get_results(self):
        return self.results
