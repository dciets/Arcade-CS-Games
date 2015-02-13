import minigame

class Singleplayer(minigame.Minigame):
    game_type = minigame.SINGLEPLAYER

    def get_results(self):
        results = [True, True]
        results[self.game.active_player] = self.get_result()
        return results

