import minigame
import pygame
import input_map


class BlackCat(minigame.Minigame):
    game_type = minigame.MULTIPLAYER
    name = 'Get on the other side!'
    cat_images = [pygame.image.load('./res/img/cat_1.png'), pygame.image.load('./res/img/cat_2.png')]

    def __init__(self, game):
        minigame.Minigame.__init__(self, game)

        self.w, self.h = self.screen.get_size()
        self.street_height = 400
        self.street_rect = pygame.Rect(0, 100, self.w, self.street_height)
        self.street_line = pygame.Rect(0, 100 + self.street_height/2 - 10, self.w, 20)

        self.cats = [[self.w/4, 520], [3*self.w/4, 520]]
        self.row_height = 100
        self.cars = [[], [], [], []]
        for i in range(4):
            for j in range(6):
                self.cars[i].append(j*100)

    def tick(self):
        self.update()
        self.draw()

    def get_results(self):
        return [True, True]
        # results = [False, False]
        # for i in range(2):
        #     if self.cats[i][1] < 100:
        #         results[i] = True
        # return results

    def draw(self):
        self.screen.fill((0, 100, 0))

        pygame.draw.rect(self.screen, (0, 0, 0), self.street_rect)
        pygame.draw.rect(self.screen, (255, 255, 0), self.street_line)
        x = 25
        while x < self. w:
            y1 = 100 + self.street_height/4 - 5
            y2 = 100 + 3*self.street_height/4 - 5
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(x, y1, 50, 10))
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(x, y2, 50, 10))
            x += 100

        for i in range(2):
            self.screen.blit(BlackCat.cat_images[i], pygame.Rect(self.cats[i][0], self.cats[i][1], 50, 50))

        for i in range(4):
            for car in self.cars[i]:
                y = 125 + i*100
                pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(car, y, 80, 50))

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                for i in range(2):
                    if event.key == input_map.PLAYERS_MAPPING[i][input_map.UP]:
                        print 'Player ' + str(i) + ' UP'
                        self.cats[i][1] -= self.row_height
                    elif event.key == input_map.PLAYERS_MAPPING[i][input_map.DOWN]:
                        self.cats[i][1] += self.row_height