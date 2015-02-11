from datetime import datetime, timedelta
import splash

class Minigame:
    '''Play a minigame!'''
    def __init__(self, game):
        self.game = game
        self.minigame = self.game.minigame(self.game.difficulty)
        self.duration = self.minigame.get_duration()
        self.started_at = datetime.now()
        print('In minigame!')

    def run(self):
        if(self.started_at + timedelta(seconds=self.duration) < datetime.now()):
            results = self.minigame.get_results()
            for player, result in zip(self.game.players, results):
                if not result:
                    player.lives -= 1
            self.game.state = splash.Splash(self.game)

            if all(results):
                self.game.difficulty += 1
