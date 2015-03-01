import pygame
from pygame.sprite import Sprite
import os


class PlayerState:
    GROUND = 0
    JUMPING = 1


class Player(Sprite):
    IMAGE_DIRECTORY = "res/img/its_raining_beer/"
    SPEED = 0.7

    def __init__(self, name, position, width, *groups):
        super(Player, self).__init__(*groups)
        self.name = name
        self.x, self.y = position
        self.ticks = 0
        self.width = width
        self.direction = 0
        self.state = PlayerState.GROUND
        self.velocity = 0
        self.still_counter = 0
        self.image_id = 0
        self.score = 0
        self.images = {-1: [], 0: [], 1: []}
        self._load_images()
        self.width, self.height = self.images[1][self.image_id].get_size()
        self._change_rect(self.x, self.y, self.width, self.height)

    def move(self, direction, game_rect, other_player):
        self.ticks += 1
        self.direction = direction

        if self.state == PlayerState.GROUND and self.y < game_rect.height and not self.rect.colliderect(other_player.rect):
            self.state = PlayerState.JUMPING
            self.velocity = 0

        # Vertical speed
        new_y = self.y
        if self.state == PlayerState.JUMPING:
            self.velocity -= 0.03
            new_y -= self.velocity
            if new_y >= game_rect.height:
                new_y = game_rect.height
                self.state = PlayerState.GROUND
                self.velocity = 0

        # Horizontal speed
        new_x = self.x + self.SPEED * self.direction

        # Collisions
        test_rect = pygame.Rect(new_x, new_y, self.width, self.height)
        if test_rect.colliderect(other_player.rect):
            if other_player.rect.centerx - test_rect.centerx < test_rect.width:
                if test_rect.y < other_player.rect.y:
                    new_y = other_player.rect.top - self.height + 1
                    self.state = PlayerState.GROUND
                elif test_rect.y > other_player.rect.y:
                    new_y = self.y
                else:
                    new_x = self.x

        if new_x > 0 and new_x + self.width < game_rect.width:
            self.x = new_x
        self.y = new_y

        self._change_rect(self.x, self.y, self.width, self.height)

    def jump(self):
        if self.state == PlayerState.GROUND:
            self.state = PlayerState.JUMPING
            self.velocity = 4

    def blit(self, screen):
        if self.ticks % 30 == 0:
            self.image_id += 1
            self.image_id %= len(self.images[self.direction])
        elif self.image_id >= len(self.images[self.direction]):
            self.image_id = 0

        direction = self.direction
        if self.state == PlayerState.JUMPING:
            if direction == 0:
                direction = 1
            self.image_id = 2

        screen.blit(self.images[direction][self.image_id], (self.x, self.y))

    def _change_rect(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def _load_images(self):
        for f in sorted(os.listdir("res/img/its_raining_beer/")):
            if f.startswith(self.name) and f.endswith(".png"):
                image = pygame.image.load(self.IMAGE_DIRECTORY + f).convert_alpha()
                height2 = int((float(image.get_height()) / image.get_width()) * self.width)
                image = pygame.transform.scale(image, (self.width, height2))
                self.images[1].append(image)
                self.images[-1].append(pygame.transform.flip(self.images[1][-1], True, False))
        self.images[0] = [self.images[1][0]]
        del self.images[-1][0]
        del self.images[1][0]
