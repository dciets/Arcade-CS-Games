import pygame
from pygame.locals import *
import splash

class Menu:
    '''
    Display the initial menu waiting for play to get ready
    and pick universities.
    '''
    def __init__(self, game):
        self.game = game
        self.insert_coin_txt = game.font.render("Insert coin...", 0, (255,255,255))
        self.insert_coin_rect = self.insert_coin_txt.get_rect()
        self.insert_coin_rect.topleft = (50, 300)

    def run(self):
        # Show game menu
        # Perhaps something that await two player input
        # while display "Insert coins..."

        self.game.screen.fill((0,0,0))
        self.game.screen.blit(self.insert_coin_txt, self.insert_coin_rect)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                self.start_game()

    def start_game(self):
        self.game.state = splash.Splash(self.game)

