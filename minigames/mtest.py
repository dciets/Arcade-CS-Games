import minigame

class MTest(minigame.Minigame):
    game_type = minigame.MULTIPLAYER

    def run(self):
        pass

    def get_results(self):
        return [False, False]
