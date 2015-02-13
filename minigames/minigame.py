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
    max_duration = 5.0
    def __init__(self, difficulty, screen, font):
        self.screen = screen
        self.font = font
        self.difficulty = difficulty
        self.started_at = pygame.time.get_ticks()

    def run(self):
        '''Should be overriden by minigame implementation'''
        self.screen.fill((0,0,0))

        self.tick()

        elapsed_ms = pygame.time.get_ticks() - self.started_at
        duration = self.get_duration()

        sec_left = str(int(duration - elapsed_ms/1000) - 1)
        self.print_msg(sec_left, (30, 550))


    def get_duration(self):
        '''Return minigame duration, can depend on self.difficulty'''
        return self.max_duration / (self.difficulty+1)

    def get_results(self):
        '''
        Return players' results. A False result means that a
        player failed while a True result means that a player succeed
        '''
        return [True, True]

    def print_msg(self, msg, topleft, color = (255,255,255)):
        msg_sf = self.font.render(msg, 0, color)
        rect = msg_sf.get_rect()
        rect.topleft = topleft
        self.screen.blit(msg_sf, rect)

