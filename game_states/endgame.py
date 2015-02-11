from datetime import datetime, timedelta

class EndGame:
    '''Display end game score'''
    def __init__(self, game):
        self.game = game
        self.started_at = datetime.now()
        print('In end game screen')

    def run(self):
        if(self.started_at + timedelta(seconds=0) < datetime.now()):
            self.game.stop()

