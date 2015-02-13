import minigame
import input_map

class Minigame(minigame.Minigame):
    game_type = minigame.SINGLEPLAYER

    def get_results(self):
        results = [True, True]
        results[self.game.active_player] = self.get_result()
        return results

    def get_player_keys(self):
        print input_map.get_player_keys(self.game.active_player)
        return input_map.get_player_keys(self.game.active_player)

