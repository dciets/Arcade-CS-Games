import minigame

class STest(minigame.Minigame):
    game_type = minigame.SINGLEPLAYER

    def run():
        pass

    def get_results(self):
        return [False, True]
