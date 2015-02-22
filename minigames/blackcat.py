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
        # Street stuff
        self.street_height = 4*self.h/6
        self.row_height = self.h/6
        self.street_rect = pygame.Rect(0, self.h/6, self.w, self.street_height)
        self.street_line = pygame.Rect(0, self.h/6 + self.street_height/2 - self.h/60, self.w, self.h/30)
        self.street_bars = []
        x = 25
        while x < self. w:
            y1 = self.h/6 + self.street_height/4 - 5
            y2 = self.h/6 + 3*self.street_height/4 - 5
            self.street_bars.append(pygame.Rect(x, y1, self.w/16, self.h/60))
            self.street_bars.append(pygame.Rect(x, y2, self.w/16, self.h/60))
            x += self.w/8

        # Cat stuff
        self.cats = [
            pygame.Rect(self.w/4, 5*self.h/6 + self.h/24, self.w/16, self.h/12),
            pygame.Rect(3*self.w/4, 5*self.h/6 + self.h/24, self.w/16, self.h/12)
        ]
        self.dead = [False, False]

        # Car stuff
        self.cars = [[], [], [], []]
        for i in range(4):
            y = 0.208*self.h + i*self.h/6
            for j in range(self.difficulty+1):
                self.cars[i].append(pygame.Rect(j*self.w/4 + i * self.w/16, y, self.w/10, self.h/12))

    def tick(self):
        self.update()
        self.draw()

    def get_results(self):
        results = [False, False]
        for cat in self.cats:
            if cat.y < self.h/6:
                results[self.cats.index(cat)] = True
        return results

    def draw(self):
        self.screen.fill((0, 100, 0))
        pygame.draw.rect(self.screen, (0, 0, 0), self.street_rect)
        pygame.draw.rect(self.screen, (255, 255, 0), self.street_line)
        for bar in self.street_bars:
            pygame.draw.rect(self.screen, (255, 255, 255), bar)
        for cat in self.cats:
            i = self.cats.index(cat)
            if not self.dead[i]:
                self.screen.blit(BlackCat.cat_images[i], self.cats[i])
            else:
                self.screen.blit(BlackCat.blood_image, self.cats[i])
        for row in self.cars:
            for car in row:
                pygame.draw.rect(self.screen, (255, 0, 0), car)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                for i in range(2):
                    if event.key == input_map.PLAYERS_MAPPING[i][input_map.UP] and not self.dead[i]:
                        if self.cats[i][1] > self.h/6:
                            self.cats[i][1] -= self.row_height
                    elif event.key == input_map.PLAYERS_MAPPING[i][input_map.DOWN] and not self.dead[i]:
                        if self.cats[i][1] < 5*self.h/6:
                            self.cats[i][1] += self.row_height

        for i in range(4):
            for j in range(len(self.cars[i])):
                car = self.cars[i][j]
                if i < 2:
                    car.x -= 1
                    if car.x + car.w < 0:
                        car.x = self.w
                else:
                    car.x += 1
                    if car.x > self.w:
                        car.x = -car.w
                for cat in self.cats:
                    if car.x < cat.centerx < car.x + car.w:
                        if car.y < cat.centery < car.y + car.h:
                            self.dead[self.cats.index(cat)] = True