from itertools import cycle
import pygame
from pygame.rect import Rect
from game_states.OverlayedState import OverlayedState

SINGLEPLAYER = 1
MULTIPLAYER = 2

class Minigame:
    COUNTDOWN_SPRITES = pygame.image.load("./res/img/ui/bomb.png")

    '''
    Implement shared code to minigame such as time left or
    players' input.

    self.difficulty get incremented each time this minigame
    get played, starting from 0.
    '''
    max_duration = 5000

    @classmethod
    def is_singleplayer(klass):
        return klass.game_type == SINGLEPLAYER

    def __init__(self, game):
        # Countdown timer GFX
        self.ct_bomb = pygame.transform.scale2x(Minigame.COUNTDOWN_SPRITES.subsurface(Rect((0, 0), (16, 16))).convert_alpha())
        self.ct_base_string = pygame.transform.scale2x(Minigame.COUNTDOWN_SPRITES.subsurface(Rect((17, 0), (16, 16))).convert_alpha())
        self.ct_string = pygame.transform.scale2x(Minigame.COUNTDOWN_SPRITES.subsurface(Rect((34, 0), (4, 16))).convert_alpha())
        self.ct_sparks = cycle([pygame.transform.scale2x(Minigame.COUNTDOWN_SPRITES.subsurface(Rect((39, 0), (16, 16))).convert_alpha()),
                                pygame.transform.scale2x(Minigame.COUNTDOWN_SPRITES.subsurface(Rect((39, 17), (16, 16))).convert_alpha())])
        self.ct_spark = self.ct_sparks.next()
        self.ct_one = pygame.transform.scale2x(Minigame.COUNTDOWN_SPRITES.subsurface(Rect((0, 17), (11, 16))).convert_alpha())
        self.ct_two = pygame.transform.scale2x(Minigame.COUNTDOWN_SPRITES.subsurface(Rect((12, 17), (11, 16))).convert_alpha())
        self.ct_three = pygame.transform.scale2x(Minigame.COUNTDOWN_SPRITES.subsurface(Rect((24, 17), (11, 16))).convert_alpha())
        self.ct_explosion = pygame.transform.scale2x(Minigame.COUNTDOWN_SPRITES.subsurface(Rect((0, 34), (48, 48))).convert_alpha())

        # Score markers
        self.score = []
        self.score_marker_1 = pygame.image.load('res/img/ui/score1.png').convert_alpha()
        self.score_marker_2 = pygame.image.load('res/img/ui/score2.png').convert_alpha()

        self.game = game
        self.fps = game.FPS
        self.elapsed_ms = 0
        self.frame = 0
        self.screen = game.screen
        self.font = game.font
        self.gfx = game.gfx
        self.difficulty = game.difficulty
        self.sec_left = 0

    def init(self):
        '''Should be overriden by minigame implementation'''
        pass

    def tick(self):
        '''Should be overriden by minigame implementation'''
        pass

    def run(self):
        self.elapsed_ms = self.game.state.elapsed_ms
        self.screen.fill((0,0,0))
        self.tick()
        self.frame += 1

    def display_score_markers(self):
        self.game.border.blit(self.score_marker_1, self.score_marker_1.get_rect(topleft=(350, 5)))
        self.game.border.blit(self.score_marker_2, self.score_marker_2.get_rect(topleft=(450, 5)))

    def display_overlay(self):
        self.sec_left = int((self.get_duration() - self.elapsed_ms)/1000)

        spark_x = 32
        spark_y = self.game.SCREEN_HEIGHT - 24

        if self.sec_left == 1:
            self.game.border.blit(self.ct_explosion, self.ct_explosion.get_rect(bottomleft=(0, self.game.SCREEN_HEIGHT)))
        elif self.sec_left > 1:
            self.game.border.blit(self.ct_bomb, self.ct_bomb.get_rect(bottomleft=(0, self.game.SCREEN_HEIGHT)))

            if self.sec_left > 2:
                spark_x += 32
                spark_y = self.game.SCREEN_HEIGHT
                self.game.border.blit(self.ct_base_string, self.ct_base_string.get_rect(bottomleft=(32, self.game.SCREEN_HEIGHT)))

                if self.sec_left > 3:
                    for t in range(0, self.sec_left - 3):
                        for i in range(0, 10):
                            spark_x += 8
                            self.game.border.blit(self.ct_string, self.ct_string.get_rect(bottomleft=(64 + (t * 80) + (i * 8), self.game.SCREEN_HEIGHT)))

            if self.sec_left == 2:
                self.game.border.blit(self.ct_one, self.ct_one.get_rect(bottomleft=(8, self.game.SCREEN_HEIGHT - 40)))
            elif self.sec_left == 3:
               self.game.border.blit(self.ct_two, self.ct_two.get_rect(bottomleft=(8, self.game.SCREEN_HEIGHT - 40)))
            elif self.sec_left == 4:
               self.game.border.blit(self.ct_three, self.ct_three.get_rect(bottomleft=(8, self.game.SCREEN_HEIGHT - 40)))

            if self.frame % 4 == 0 or (self.frame % 3 == 0 and self.sec_left == 2):
                self.ct_spark = self.ct_sparks.next()

            self.game.border.blit(self.ct_spark, self.ct_spark.get_rect(bottomleft=(spark_x, spark_y)))

    def get_duration(self):
        '''Return minigame duration, can depend on self.difficulty'''
        return self.max_duration

    def get_results(self):
        '''
        Return players' results. A False result means that a
        player failed while a True result means that a player succeed
        '''
        return [True, True]

