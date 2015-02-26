import minigame
import pygame
from input_map import *


class ShootTargets(minigame.Minigame):

    name = 'Shoot targets'
    game_type = minigame.MULTIPLAYER

    damp = 15.0
    speed = 20
    flare = pygame.image.load('res/img/shoot_targets/flare.png')

    def __init__(self, game):
        minigame.Minigame.__init__(self, game)
        
        player1_image = pygame.image.load('res/img/shoot_targets/player1.png')
        player2_image = pygame.image.load('res/img/shoot_targets/player2.png')

        self.game = game
        self.players = [
            {'image': player1_image,
             'position': player1_image.get_rect(),
             'target_position': [0, 0],
             'direction': [0, 0],
             'points': 0, },

            {'image': player2_image,
             'position': player2_image.get_rect(),
             'target_position': [0, 0],
             'direction': [0, 0],
             'points': 0, },
        ]

    def tick(self):
        keys = pygame.key.get_pressed()
        flares = [False, False]

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                for i in range(len(self.players)):
                    if event.key == PLAYERS_MAPPING[i][ACTION]:
                        flares[i] = True

        for i in range(len(self.players)):
            if keys[PLAYERS_MAPPING[i][LEFT]]:
                self.players[i]['direction'][0] = -1
            elif keys[PLAYERS_MAPPING[i][RIGHT]]:
                self.players[i]['direction'][0] = 1
            else:
                self.players[i]['direction'][0] = 0

            if keys[PLAYERS_MAPPING[i][UP]]:
                self.players[i]['direction'][1] = -1
            elif keys[PLAYERS_MAPPING[i][DOWN]]:
                self.players[i]['direction'][1] = 1
            else:
                self.players[i]['direction'][1] = 0

        for i, player in enumerate(self.players):
            player['target_position'][0] += player['direction'][0] * ShootTargets.speed
            player['target_position'][1] += player['direction'][1] * ShootTargets.speed

            player['position'].centerx += (player['target_position'][0] - player['position'].centerx) / ShootTargets.damp
            player['position'].centery += (player['target_position'][1] - player['position'].centery) / ShootTargets.damp
        
        self.screen.fill((20, 21, 32))

        for i, player in enumerate(self.players):            
            if flares[i]:
                rect = ShootTargets.flare.get_rect()
                rect.center = player['position'].center

                self.screen.blit(ShootTargets.flare, rect)

            self.screen.blit(player['image'], player['position'])
