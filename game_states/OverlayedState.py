import pygame
import gfx

class OverlayedState:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font('res/font/ps2p.ttf', 14)
        self.border_gfx = pygame.image.load('res/img/ui/minigame_overlay.png').convert_alpha()
        self.heart = pygame.image.load('res/img/ui/heart.png').convert_alpha()

    def display_hud(self):
        player1_name = self.font.render(self.game.players[0].university, 0, (255, 0, 0))
        player2_name = self.font.render(self.game.players[1].university, 0, (0, 0, 255))

        self.game.border.blit(self.border_gfx, (0,0))

        # Display players names
        self.game.border.blit(player1_name, player1_name.get_rect(topleft=(98, 5)))
        self.game.border.blit(player2_name, player2_name.get_rect(topleft=(578, 5)))

        # Display player lives
        for i in range(self.game.players[0].lives):
            self.game.border.blit(self.heart, self.heart.get_rect(topleft=(31, 23 + i * 61)))

        for i in range(self.game.players[0].lives):
            self.game.border.blit(self.heart, self.heart.get_rect(topleft=(727, 23 + i * 61)))