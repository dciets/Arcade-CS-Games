import random
from beer import Beer


class BeerManager():

    def __init__(self, max_beers, default_speed, game_size):
        self.max_beers = max_beers
        self.default_speed = default_speed
        self.width, self.height = game_size
        self.beers = []
        self.ticks = 0

    def update(self):
        self.ticks += 1

        if len(self.beers) < self.max_beers:
            if self.ticks % 200 == 0:
                self.beers.append(Beer((random.randint(20, self.width - 20), -50), int(0.05 * self.width), self.default_speed + random.random() * 0.25))

        for beer in self.beers:
            beer.move()

        self._delete_beers([beer for beer in self.beers if beer.rect.y > self.height])

    def detect_collision(self, player):
        old_beers = []
        for beer in self.beers:
            if player.rect.colliderect(beer.rect):
                old_beers.append(beer)
                player.score += 1
        self._delete_beers(old_beers)

    def blit(self, screen):
        for beer in self.beers:
            beer.blit(screen)

    def _delete_beers(self, old_beers):
        for beer in old_beers:
            beer.kill()
            self.beers.remove(beer)