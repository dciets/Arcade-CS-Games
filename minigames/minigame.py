import pygame

SINGLEPLAYER = 1
MULTIPLAYER = 2

class Minigame:
    '''
    Implement shared code to minigame such as time left or
    players' input.

    self.difficulty get incremented each time this minigame
    get played, starting from 0.
    '''
    max_duration = 10000

    @classmethod
    def is_singleplayer(klass):
        return klass.game_type == SINGLEPLAYER

    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = game.font
        self.gfx = game.gfx
        self.difficulty = game.difficulty
        self.started_at = pygame.time.get_ticks()

    def init(self): pass
    def tick(self): pass

    def run(self):
        '''Should be overriden by minigame implementation'''
        self.screen.fill((0,0,0))

        self.tick()

        elapsed_ms = pygame.time.get_ticks() - self.started_at
        duration = self.get_duration()

        sec_left = str(int((duration - elapsed_ms)/1000))
        self.gfx.print_msg(sec_left, (30, 550))

    def get_duration(self):
        '''Return minigame duration, can depend on self.difficulty'''
        return self.max_duration

    def get_results(self):
        '''
        Return players' results. A False result means that a
        player failed while a True result means that a player succeed
        '''
        return [True, True]

