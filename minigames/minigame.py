SINGLEPLAYER = 1
MULTIPLAYER = 2

class Minigame:
    '''
    Implement shared code to minigame such as time left or
    players' input.

    self.difficulty get incremented each time this minigame
    get played, starting from 0.
    '''
    max_duration = 0.0
    def __init__(self, difficulty):
        self.difficulty = difficulty

    def tick(self, dt):
        '''Should be overriden by minigame implementation'''
        pass

    def get_duration(self):
        '''Return minigame duration, can depend on self.difficulty'''
        return self.max_duration / (self.difficulty+1)

    def get_results(self):
        '''
        Return players' results. A False result means that a
        player failed while a True result means that a player succeed
        '''
        return [True, True]

