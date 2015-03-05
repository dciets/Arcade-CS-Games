import minigame
import pygame
import input_map
import random


class BlackCat(minigame.Minigame):
    game_type = minigame.MULTIPLAYER
    name = 'Get to the other side!'
    cat_images = [pygame.image.load('./res/img/blackcat/cat_1.png'), pygame.image.load('./res/img/blackcat/cat_2.png')]
    blood_image = pygame.image.load('./res/img/blackcat/blood.png')
    CAR = 0
    TRUCK = 1
    CAR_MODELS = [
        {'image': pygame.image.load('./res/img/blackcat/car_blue.png'), 'width': 80, 'height': 40, 'speed': 2},
        {'image': pygame.image.load('./res/img/blackcat/truck.png'), 'width': 160, 'height': 53, 'speed': 1}
    ]
    CAR_PATTERNS = [
        [  # Difficulty 0
            [{'model': TRUCK, 'lane': 0, 'x': 600}, {'model': TRUCK, 'lane': 3, 'x': 100}, {'model': TRUCK, 'lane': 1, 'x': 400}, {'model': TRUCK, 'lane': 2, 'x': 400}],
            [{'model': CAR, 'lane': 0, 'x': 600}, {'model': CAR, 'lane': 3, 'x': 100}, {'model': CAR, 'lane': 1, 'x': 500}, {'model': CAR, 'lane': 2, 'x': 200}]
        ],
        [  # Difficulty 1
            [{'model': TRUCK, 'lane': 0, 'x': 600}, {'model': TRUCK, 'lane': 3, 'x': 100}, {'model': CAR, 'lane': 1, 'x': 400}, {'model': CAR, 'lane': 2, 'x': 400}],
            [{'model': CAR, 'lane': 0, 'x': 600}, {'model': CAR, 'lane': 3, 'x': 100}, {'model': TRUCK, 'lane': 1, 'x': 400}, {'model': TRUCK, 'lane': 2, 'x': 400}]
        ],
        [  # Difficulty 2
            [{'model': TRUCK, 'lane': 0, 'x': 600}, {'model': TRUCK, 'lane': 0, 'x': 420}, {'model': TRUCK, 'lane': 3, 'x': 100}, {'model': TRUCK, 'lane': 3, 'x': 280}, {'model': CAR, 'lane': 1, 'x': 400}, {'model': CAR, 'lane': 2, 'x': 400}],
            [{'model': TRUCK, 'lane': 0, 'x': 600}, {'model': CAR, 'lane': 1, 'x': 500}, {'model': TRUCK, 'lane': 3, 'x': 100}, {'model': CAR, 'lane': 2, 'x': 280}, {'model': CAR, 'lane': 1, 'x': 400}, {'model': CAR, 'lane': 2, 'x': 400}]
        ],
        [
            [{'model': TRUCK, 'lane': 0, 'x': 600}, {'model': TRUCK, 'lane': 0, 'x': 420}, {'model': TRUCK, 'lane': 3, 'x': 100}, {'model': TRUCK, 'lane': 3, 'x': 280}, {'model': CAR, 'lane': 1, 'x': 400}, {'model': CAR, 'lane': 2, 'x': 400}, {'model': CAR, 'lane': 1, 'x': 500}, {'model': CAR, 'lane': 2, 'x': 280}],
            [{'model': CAR, 'lane': 0, 'x': 600}, {'model': CAR, 'lane': 0, 'x': 500}, {'model': CAR, 'lane': 3, 'x': 100}, {'model': CAR, 'lane': 3, 'x': 200}, {'model': CAR, 'lane': 1, 'x': 400}, {'model': CAR, 'lane': 2, 'x': 400}, {'model': CAR, 'lane': 1, 'x': 500}, {'model': CAR, 'lane': 2, 'x': 280}]
        ],
        [
            [{'model': TRUCK, 'lane': 0, 'x': 600}, {'model': TRUCK, 'lane': 0, 'x': 420}, {'model': TRUCK, 'lane': 0, 'x': 240}, {'model': TRUCK, 'lane': 3, 'x': 100}, {'model': TRUCK, 'lane': 3, 'x': 280}, {'model': TRUCK, 'lane': 3, 'x': 460}, {'model': CAR, 'lane': 1, 'x': 600}, {'model': CAR, 'lane': 1, 'x': 700}, {'model': CAR, 'lane': 2, 'x': 100}, {'model': CAR, 'lane': 2, 'x': 200}],
            [{'model': TRUCK, 'lane': 0, 'x': 600}, {'model': TRUCK, 'lane': 0, 'x': 200}, {'model': TRUCK, 'lane': 3, 'x': 100}, {'model': TRUCK, 'lane': 3, 'x': 500}, {'model': CAR, 'lane': 1, 'x': 600}, {'model': CAR, 'lane': 1, 'x': 400}, {'model': CAR, 'lane': 2, 'x': 100}, {'model': CAR, 'lane': 2, 'x': 300}]
        ]
    ]

    def __init__(self, game):
        minigame.Minigame.__init__(self, game)
        if self.difficulty > 4: self.difficulty = 4
        self.width = game.GAME_WIDTH
        self.height = game.GAME_HEIGHT
        # Street stuff
        self.street_height = 400
        self.row_height = 100
        self.street_rect = pygame.Rect(0, 75, self.width, self.street_height)
        self.street_line = pygame.Rect(0, 75 + self.street_height/2 - 10, self.width, 20)
        self.street_bars = []
        x = 25
        while x < self.width:
            y1 = 75 + self.street_height/4 - 5
            y2 = 75 + 3*self.street_height/4 - 5
            self.street_bars.append(pygame.Rect(x, y1, 50, 10))
            self.street_bars.append(pygame.Rect(x, y2, 50, 10))
            x += 100

        # Cat stuff
        self.cats = [
            pygame.Rect(self.width/4, 5*self.height/6 + 50, 50, 50),
            pygame.Rect(3*self.width/4, 5*self.height/6 + 50, 50, 50)
        ]
        self.dead = [False, False]

        # Car stuff
        self.cars = []
        pattern_pool = BlackCat.CAR_PATTERNS[self.difficulty]
        pattern = random.choice(pattern_pool)
        for car in pattern:
            car_model = BlackCat.CAR_MODELS[car['model']]
            image = car_model['image'] if int(car['lane']/2) else pygame.transform.flip(car_model['image'], True, False)
            self.cars.append({
                'image': image,
                'rect': pygame.Rect(car['x'] - car_model['width']/2, 100 + car['lane']*100, car_model['width'], car_model['height']),
                'lane': car['lane'],
                'speed': car_model['speed']
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
                        if self.cats[i][1] > 25:
                            self.cats[i][1] -= self.row_height
                    elif event.key == input_map.PLAYERS_MAPPING[i][input_map.DOWN] and not self.dead[i]:
                        if self.cats[i][1] < 475:
                            self.cats[i][1] += self.row_height

        for car in self.cars:
            if car['lane'] < 2:
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