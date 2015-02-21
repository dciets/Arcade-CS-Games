import minigame
import pygame
import input_map


class BlackCat(minigame.Minigame):
    game_type = minigame.MULTIPLAYER
    name = 'Get on the other side!'
    cat_images = [pygame.image.load('./res/img/blackcat/cat_1.png'), pygame.image.load('./res/img/blackcat/cat_2.png')]
    blood_image = pygame.image.load('./res/img/blackcat/blood.png')

    def __init__(self, game):
        minigame.Minigame.__init__(self, game)
        self.w, self.h = self.screen.get_size()
        self.street_height = 400
        self.street_rect = pygame.Rect(0, 100, self.w, self.street_height)
        self.street_line = pygame.Rect(0, 100 + self.street_height/2 - 10, self.w, 20)

        self.cats = [[self.w/4, 520], [3*self.w/4, 520]]
        self.dead = [False, False]
        self.row_height = 100
        self.cars = [[], [], [], []]
        for i in range(4):
            for j in range(self.difficulty+1):
                self.cars[i].append(j*200 + i* 50)

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
            if not self.dead[i]:
                self.screen.blit(BlackCat.cat_images[i], pygame.Rect(self.cats[i][0], self.cats[i][1], 50, 50))
            else:
                self.screen.blit(BlackCat.blood_image, pygame.Rect(self.cats[i][0], self.cats[i][1], 50, 50))

        for i in range(4):
            for car in self.cars[i]:
                y = 125 + i*100
                pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(car, y, 60, 50))

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                for i in range(2):
                    if event.key == input_map.PLAYERS_MAPPING[i][input_map.UP] and not self.dead[i]:
                        if self.cats[i][1] > 100:
                            self.cats[i][1] -= self.row_height
                    elif event.key == input_map.PLAYERS_MAPPING[i][input_map.DOWN] and not self.dead[i]:
                        if self.cats[i][1] < 500:
                            self.cats[i][1] += self.row_height

        for i in range(4):
            for j in range(len(self.cars[i])):
                y = 125 + i*100
                if i < 2:
                    self.cars[i][j] -= 1
                    if self.cars[i][j] + 80 < 0:
                        self.cars[i][j] = self.w
                else:
                    self.cars[i][j] += 1
                    if self.cars[i][j] > self.w:
                        self.cars[i][j] = -80
                for c in range(2):
                    if self.cars[i][j] < self.cats[c][0]+25 < self.cars[i][j] + 80:
                        if y < self.cats[c][1]+25 < y + 50:
                            self.dead[c] = True