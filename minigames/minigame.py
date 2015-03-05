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
    max_duration = 5000

    @classmethod
    def is_singleplayer(klass):
        return klass.game_type == SINGLEPLAYER

    def __init__(self, game):
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
        self.sec_left = str(int((self.get_duration() - self.elapsed_ms)/1000))
        self.gfx.print_msg(self.sec_left, (15, 515))

    def get_duration(self):
        '''Return minigame duration, can depend on self.difficulty'''
        return self.max_duration

    def get_results(self):
        '''
        Return players' results. A False result means that a
        player failed while a True result means that a player succeed
        '''
        return [True, True]

