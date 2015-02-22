import minigame
import pygame
import input_map


class BlackCat(minigame.Minigame):
    game_type = minigame.MULTIPLAYER
    name = 'Get on the other side!'
    cat_images = [pygame.image.load('./res/img/blackcat/cat_1.png'), pygame.image.load('./res/img/blackcat/cat_2.png')]
    blood_image = pygame.image.load('./res/img/blackcat/blood.png')
    CAR = 0
    TRUCK = 1
    CAR_MODELS = [
        {'image': pygame.image.load('./res/img/blackcat/car_blue.png'), 'width': 80, 'height': 40, 'speed': 2},
        {'image': pygame.image.load('./res/img/blackcat/truck.png'), 'width': 160, 'height': 53, 'speed': 1}
    ]
    # Add CAR_PATTERNS [[[{}, {}], [{}, {}]], [[{}, {}], [{}, {}]], [[{}, {}], [{}, {}]], ...]
    # Difficulty is the index, then you pick one at random.
    # Each patterns as [{'model':car_model, 'x':x_pos_of_car, 'y':y_pos_of_car, 'side':side_of_street(0 or 1)}]

    def __init__(self, game):
        minigame.Minigame.__init__(self, game)
        self.width, self.height = self.screen.get_size()
        # Street stuff
        self.street_height = 400
        self.row_height = 100
        self.street_rect = pygame.Rect(0, 100, self.width, self.street_height)
        self.street_line = pygame.Rect(0, 100 + self.street_height/2 - 10, self.width, 20)
        self.street_bars = []
        x = 25
        while x < self.width:
            y1 = 100 + self.street_height/4 - 5
            y2 = 100 + 3*self.street_height/4 - 5
            self.street_bars.append(pygame.Rect(x, y1, 50, 10))
            self.street_bars.append(pygame.Rect(x, y2, 50, 10))
            x += 100

        # Cat stuff
        self.cats = [
            pygame.Rect(self.width/4, 5*self.height/6 + 25, 50, 50),
            pygame.Rect(3*self.width/4, 5*self.height/6 + 25, 50, 50)
        ]
        self.dead = [False, False]

        # Car stuff
        self.cars = []
        for i in range(4):
            y = 125 + i*100
            for j in range(self.difficulty+1):
                if i == 0 or i == 3:
                    model = BlackCat.TRUCK
                else:
                    model = BlackCat.CAR
                image = BlackCat.CAR_MODELS[model]['image'] if int(i/2) else pygame.transform.flip(BlackCat.CAR_MODELS[model]['image'], True, False)
                self.cars.append({
                    'image': image,
                    'rect': pygame.Rect(j*self.width/4 + i * self.width/16, y, BlackCat.CAR_MODELS[model]['width'], BlackCat.CAR_MODELS[model]['height']),
                    'side': int(i/2),
                    'speed': BlackCat.CAR_MODELS[model]['speed']
                })

    def tick(self):
        self.update()
        self.draw()

    def get_results(self):
        results = [False, False]
        for cat in self.cats:
            if cat.y < 100:
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
        for car in self.cars:
            self.screen.blit(car['image'], car['rect'])

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

        for car in self.cars:
            if car['side'] == 0:
                car['rect'].x -= car['speed']
                if car['rect'].x + car['rect'].width < 0:
                    car['rect'].x = self.width
            else:
                car['rect'].x += car['speed']
                if car['rect'].x > self.width:
                    car['rect'].x = -car['rect'].width
            for cat in self.cats:
                if car['rect'].x < cat.centerx < car['rect'].x + car['rect'].w:
                    if car['rect'].y < cat.centery < car['rect'].y + car['rect'].h:
                        self.dead[self.cats.index(cat)] = True