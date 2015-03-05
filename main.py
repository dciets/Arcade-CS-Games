#!/usr/bin/env python2
import pygame
import game

def main():
    pygame.init()
    pygame.display.set_caption("Arcade CS Games 2015")
    font = pygame.font.Font('res/font/ps2p.ttf', 32)
    border = pygame.display.set_mode((game.Game.SCREEN_WIDTH, game.Game.SCREEN_HEIGHT))

    while True:
        app = game.Game(border, font)
        print("Start game")
        app.run()
        print("Game stop")

if __name__ == "__main__":
        main()
