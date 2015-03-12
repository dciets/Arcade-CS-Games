import pygame
import random
import gfx

class OverlayedState:
    def __init__(self, game):
        # Hah. I'm funny!
        self.player_names = [
            game.players[0].university if game.players[0].university != "McGill" or random.randint(0, 50) > 5 else "MgCil",
            game.players[1].university if game.players[1].university != "McGill" or random.randint(0, 50) > 5 else "MgCil"
        ]
        self.game = game
        self.font = pygame.font.Font('res/font/ps2p.ttf', 14)
        self.border_gfx = pygame.image.load('res/img/ui/minigame_overlay.png').convert_alpha()
        self.heart = pygame.image.load('res/img/ui/heart.png').convert_alpha()

    def display_hud(self):
        name1 = self.font.render(self.player_names[0], 0, (255, 0, 0))
        name2 = self.font.render(self.player_names[1], 0, (0, 0, 255))

        self.game.border.blit(self.border_gfx, (0, 0))

        # Display players names
        self.game.border.blit(name1, name1.get_rect(topleft=(99, 5)))
        self.game.border.blit(name2, name2.get_rect(topleft=(530, 5)))

        # Display player lives
        for i in range(self.game.players[0].lives):
            self.game.border.blit(self.heart, self.heart.get_rect(topleft=(31, 23 + i * 61)))

        for i in range(self.game.players[1].lives):
            self.game.border.blit(self.heart, self.heart.get_rect(topleft=(727, 23 + i * 61)))