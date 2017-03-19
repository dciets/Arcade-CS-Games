import pygame
import sys
from minigames import minigame
from input_map import *
from pygame.locals import *
from minigames import multiplayer
from random import randint

DARK_BLUE = (19, 15, 48)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 69, 0)
WHITE = (255, 255, 255)

COLOR_BACKGROUND = DARK_BLUE
COLOR_SHIP_1 = YELLOW
COLOR_SHIP_2 = ORANGE
COLOR_SHIP_1_BULLET = BLUE
COLOR_SHIP_2_BULLET = RED

SHIP_WIDTH = 45
SHIP_HEIGHT = 80
SHIP_SPEED = 25
SHIP_1_MISSILE_DIRECTION_X = 1
SHIP_2_MISSILE_DIRECTION_X = -1
MAX_MISSILES = 2

MISSILE_WIDTH = 30
MISSILE_HEIGHT = 15
MISSILE_SPEED = 20

STAR_COUNT = 200
STAR_WIDTH = 2
STAR_HEIGHT = 2
STAR_SPEED = 1.5

ASTEROID_WIDTH = 50
ASTEROID_HEIGHT = 50

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
OVERLAY_MARGIN_X = 48
OVERLAY_MARGIN_Y = 24
GAME_MARGIN_X = 47
GAME_MARGIN_Y = 46
BOUNDS_MIN_X = OVERLAY_MARGIN_X + GAME_MARGIN_X
BOUNDS_MAX_X = SCREEN_WIDTH - BOUNDS_MIN_X
BOUNDS_MIN_Y = OVERLAY_MARGIN_Y + GAME_MARGIN_Y
BOUNDS_MAX_Y = SCREEN_HEIGHT - BOUNDS_MIN_Y
MISSILE_MARGIN = (SHIP_WIDTH - MISSILE_WIDTH) / 2
ASTEROID_MARGIN_X = 65
ASTEROID_MARGIN_Y = 25
ASTEROID_BOUNDS_MIN_X = BOUNDS_MIN_X + ASTEROID_MARGIN_X
ASTEROID_BOUNDS_MAX_X = BOUNDS_MAX_X - ASTEROID_MARGIN_X
ASTEROID_BOUNDS_MIN_Y = BOUNDS_MIN_Y + ASTEROID_MARGIN_Y
ASTEROID_BOUNDS_MAX_Y = BOUNDS_MAX_Y - ASTEROID_MARGIN_Y
ASTEROID_COLUMNS = (ASTEROID_BOUNDS_MAX_X - ASTEROID_BOUNDS_MIN_X) / ASTEROID_WIDTH
ASTEROID_ROWS = (ASTEROID_BOUNDS_MAX_Y - ASTEROID_BOUNDS_MIN_Y) / ASTEROID_HEIGHT

# Asteroids have a 1 in x probability of spawning, depending on difficulty (value is used in a randint call)
ASTEROID_PROBABILITY = [
    4,
    6,
    8
]


class Ship(pygame.sprite.Sprite):
    def __init__(self, number):
        pygame.sprite.Sprite.__init__(self)
        self.width = SHIP_WIDTH
        self.height = SHIP_HEIGHT
        # Loading, scaling and rotating ship image corresponding to player
        self.image = pygame.transform.scale(
            pygame.transform.rotate(
                pygame.image.load("res/img/asteroid_showdown/ship_{}.png".format(number)),
                90 if number == 1 else -90
            ),
            (self.width, self.height)
        )
        self.rect = self.image.get_rect()
        self.speed = SHIP_SPEED
        self.number = number
        self.direction_y = 0

    def update(self, keys, ratio, *args):
        if keys[PLAYERS_MAPPING[self.number - 1][UP]]:
            self.rect.y -= ratio * self.speed
        if keys[PLAYERS_MAPPING[self.number - 1][DOWN]]:
            self.rect.y += ratio * self.speed

        self.check_bounds()

    def check_bounds(self):
        if self.rect.top < BOUNDS_MIN_Y:
            self.rect.top = BOUNDS_MIN_Y
            self.direction_y = 0
        elif self.rect.bottom > BOUNDS_MAX_Y:
            self.rect.bottom = BOUNDS_MAX_Y
            self.direction_y = 0


class Missile(pygame.sprite.Sprite):
    def __init__(self, rect, number):
        pygame.sprite.Sprite.__init__(self)
        self.width = MISSILE_WIDTH
        self.height = MISSILE_HEIGHT
        self.color = color
        # Loading, scaling and rotating missile image corresponding to the corresponding player
        self.image = pygame.transform.scale(
            pygame.transform.rotate(
                pygame.image.load("res/img/asteroid_showdown/missile_{}.png".format(number)),
                -90 if number == 1 else 90
            ),
            (self.width, self.height)
        )
        self.rect = self.image.get_rect()
        self.rect.centery = rect.centery
        self.rect.left = rect.left + MISSILE_MARGIN
        self.direction_x = SHIP_1_MISSILE_DIRECTION_X if number == 1 else SHIP_2_MISSILE_DIRECTION_X
        self.speed = MISSILE_SPEED

    def update(self, keys, ratio, *args):
        self.rect.x += self.direction_x * ratio * self.speed

        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.kill()


class Text:
    def __init__(self, size, message, rect):
        self.font = pygame.font.Font('res/font/ps2p.ttf', size)
        self.color = WHITE
        self.update_message(message, rect)

    def update_message(self, message, rect):
        self.message = message
        self.surface = self.font.render(message, True, self.color)
        self.rect = self.surface.get_rect()
        self.rect.centerx = rect.centerx
        self.rect.top = 1.25 * OVERLAY_MARGIN_Y

    def draw(self, surface):
        surface.blit(self.surface, self.rect)


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, left, top):
        pygame.sprite.Sprite.__init__(self)
        self.width = ASTEROID_WIDTH
        self.height = ASTEROID_HEIGHT
        self.image = pygame.transform.scale(
            pygame.image.load("res/img/asteroid_showdown/asteroid_{}.png".format(randint(1, 4))),
            (self.width, self.height)
        )
        # self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.top = top
        self.rect.left = left


class AsteroidShowdown(multiplayer.Minigame):
    name = "Asteroid Showdown"

    def init(self):
        self.results = [False, False]
        self.scores = [0, 0]
        # Setup screen
        self.display_screen = self.make_screen()
        self.background = pygame.Surface(self.display_screen.get_size())
        self.background.convert()
        # Create ships
        self.ship_1 = Ship(1)
        self.ship_2 = Ship(2)
        # Position them on their initial positions
        self.ship_1.rect.top = BOUNDS_MIN_Y
        self.ship_1.rect.left = BOUNDS_MIN_X
        self.ship_2.rect.bottom = BOUNDS_MAX_Y
        self.ship_2.rect.right = BOUNDS_MAX_X
        # Create sprite groups
        self.ship_1_missiles = pygame.sprite.Group()
        self.ship_2_missiles = pygame.sprite.Group()
        self.all_missiles = pygame.sprite.Group(self.ship_1_missiles, self.ship_2_missiles)
        self.asteroids = self.make_asteroids()
        self.all_sprites = pygame.sprite.Group(self.ship_1, self.ship_2, self.asteroids, self.all_missiles)
        self.keys = pygame.key.get_pressed()
        self.clock = pygame.time.Clock()
        self.previous_elapsed = pygame.time.get_ticks()
        self.scoreboard = Text(32, "00 | 00", self.display_screen.get_rect())
        self.stars = [[randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT)] for x in range(STAR_COUNT)]

    def make_screen(self):
        # Create screen and its rectangle for display
        display_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        display_screen.fill(COLOR_BACKGROUND)
        display_screen.convert()
        return display_screen

    def make_asteroids(self):
        group = pygame.sprite.Group()
        probability = ASTEROID_PROBABILITY[self.difficulty] if self.difficulty < len(ASTEROID_PROBABILITY) else ASTEROID_PROBABILITY[len(ASTEROID_PROBABILITY) - 1]
        for row in range(ASTEROID_ROWS):
            for column in range(ASTEROID_COLUMNS):
                if randint(0, probability) == 0:
                    asteroid = Asteroid(
                        ASTEROID_BOUNDS_MIN_X + column * ASTEROID_WIDTH,
                        ASTEROID_BOUNDS_MIN_Y + row * ASTEROID_HEIGHT
                    )
                    group.add(asteroid)

        return group

    def check_input(self):
        for event in pygame.event.get():
            # Update value of keys to pass it along to sprites later
            self.keys = pygame.key.get_pressed()
            if event.type == KEYDOWN:
                if event.key == PLAYERS_MAPPING[0][ACTION] and len(self.ship_1_missiles) < MAX_MISSILES:
                    # Pew pew
                    # Add missile to sprite groups with the correct direction
                    missile = Missile(self.ship_1.rect, 1)
                    self.ship_1_missiles.add(missile)
                    self.all_missiles.add(missile)
                    self.all_sprites.add(missile)
                elif event.key == PLAYERS_MAPPING[1][ACTION] and len(self.ship_2_missiles) < MAX_MISSILES:
                    missile = Missile(self.ship_2.rect, 2)
                    self.ship_2_missiles.add(missile)
                    self.all_missiles.add(missile)
                    self.all_sprites.add(missile)

    def check_collisions(self):
        hits_missiles_1 = pygame.sprite.groupcollide(self.ship_1_missiles, self.asteroids, True, False)
        hits_missiles_2 = pygame.sprite.groupcollide(self.ship_2_missiles, self.asteroids, True, False)
        # Check collisions between each ship's missiles and asteroids
        for missile, asteroids in hits_missiles_1.items():
            closest = asteroids[0]
            for asteroid in asteroids:
                # Get the topmost and leftmost asteroid to remove
                if asteroid.rect.left < closest.rect.left and asteroid.rect.top < closest.rect.top:
                    closest = asteroid
            closest.kill()
        for missile, asteroids in hits_missiles_2.items():
            closest = asteroids[0]
            for asteroid in asteroids:
                # Get the topmost and rightmost asteroid to remove
                if asteroid.rect.left > closest.rect.left and asteroid.rect.top < closest.rect.top:
                    closest = asteroid
            closest.kill()
        # Check collisions between missiles and ships
        for missile in self.ship_1_missiles:
            if pygame.sprite.collide_rect(missile, self.ship_2):
                # Add points to the player who scored a hit and kill the missile
                self.scores[0] += 1
                missile.kill()
        for missile in self.ship_2_missiles:
            if pygame.sprite.collide_rect(missile, self.ship_1):
                self.scores[1] += 1
                missile.kill()
        self.scoreboard.update_message("{:02d} | {:02d}".format(self.scores[0], self.scores[1]), self.display_screen.get_rect())

    def get_results(self):
        print("{} to {}".format(self.scores[0], self.scores[1]))
        player_1_wins = False
        player_2_wins = False
        if self.scores[0] > self.scores[1]:
            player_1_wins = True
        elif self.scores[0] < self.scores[1]:
            player_2_wins = True
        return [player_1_wins, player_2_wins]

    def get_duration(self):
        return 15000.0

    def tick(self):
        expected = (1.0 / 30.0) * 1000.0
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.previous_elapsed
        ratio = elapsed / expected
        self.previous_elapsed = current_time

        # Handle events
        self.check_input()
        # Fill background with stars and translate them on the screen
        self.background.fill(COLOR_BACKGROUND)
        for star in self.stars:
            pygame.draw.rect(self.background, WHITE, pygame.Rect(star[0], star[1], STAR_WIDTH, STAR_HEIGHT))
            star[0] -= ratio * STAR_SPEED
            # If a star leaves the screen through the left, move it to the right of the screen at a random height
            if star[0] < 0:
                star[0] = SCREEN_WIDTH
                star[1] = randint(0, SCREEN_HEIGHT)
        self.display_screen.blit(self.background, (0, 0))
        # Update game elements
        self.all_sprites.update(self.keys, ratio)
        self.check_collisions()
        # Drawing surface
        self.all_sprites.draw(self.display_screen)
        self.scoreboard.draw(self.display_screen)
