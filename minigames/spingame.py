import minigame
import pygame
import input_map


class SpinGame(minigame.Minigame):
    game_type = minigame.MULTIPLAYER
    name = 'Turn 7 time on yourself!'
    FRONT = 0
    LEFT = 1
    BACK = 2
    RIGHT = 3
    IMAGES = [
        pygame.image.load('./res/img/spingame/front.png'),
        pygame.image.load('./res/img/spingame/left.png'),
        pygame.image.load('./res/img/spingame/back.png'),
        pygame.image.load('./res/img/spingame/right.png'),
    ]

    def __init__(self, game):
        minigame.Minigame.__init__(self, game)
        self.difficulty = game.difficulty if game.difficulty < 5 else 5
        self.max_duration = 1000 * (8-self.difficulty)
        self.width, self.height = self.screen.get_size()
        self.player_turns = [0, 0]
        self.player_positions = [[0, 0, 0, 0], [0, 0, 0, 0]]
        self.font = pygame.font.Font('res/font/ps2p.ttf', 16)
        self.counter = 0
        self.text = self.font.render('Turn on yourself to break the bad spell!!', 0, (0, 100, 0))
        self.text_rect = self.text.get_rect()
        self.text_rect.topleft = (400 - self.text_rect.width/2, 500)

    def tick(self):
        self.update()
        self.draw()

    def get_results(self):
        results = [False, False]
        for player_turn in self.player_turns:
            if player_turn >= 7:
                results[self.player_turns.index(player_turn)] = True
        return results

    def draw(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(self.width/2-2, 0, 4, self.height))
        for i in range(2):
            txt = self.font.render(self.game.players[i].university + ': '+str(self.player_turns[i])+' Turns', 0, (255, 0, 0) if i == 0 else (0, 0, 255))
            rect = txt.get_rect()
            rect.topleft = (200 - rect.width/2 + i*400, 50)
            self.screen.blit(txt, rect)
            self.screen.blit(SpinGame.IMAGES[self.player_positions[i][-1]], pygame.Rect(152 + i*400, 220, 96, 160))

        self.screen.blit(self.text, self.text_rect)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                for i in range(2):
                    if event.key == input_map.PLAYERS_MAPPING[i][input_map.UP]:
                        self.player_positions[i].append(SpinGame.BACK)
                        self.check_turn(i)
                    elif event.key == input_map.PLAYERS_MAPPING[i][input_map.DOWN]:
                        self.player_positions[i].append(SpinGame.FRONT)
                        self.check_turn(i)
                    elif event.key == input_map.PLAYERS_MAPPING[i][input_map.LEFT]:
                        self.player_positions[i].append(SpinGame.LEFT)
                        self.check_turn(i)
                    elif event.key == input_map.PLAYERS_MAPPING[i][input_map.RIGHT]:
                        self.player_positions[i].append(SpinGame.RIGHT)
                        self.check_turn(i)

    def check_turn(self, player):
        if len(self.player_positions[player]) > 4:
            del self.player_positions[player][0]
        positions = self.player_positions[player]
        if positions[0] < positions[1] < positions[2] < positions[3]:
            self.player_turns[player] += 1
        elif positions[0] > positions[1] > positions[2] > positions[3]:
            self.player_turns[player] += 1