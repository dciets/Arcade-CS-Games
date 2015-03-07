import pygame
import operator
from explosion_sprite import ExplosionSprite


class Player:
    damp = 10.0
    speed = 20

    player_images = [
        pygame.image.load('res/img/shoot_targets/player1.png'),
        pygame.image.load('res/img/shoot_targets/player2.png'), ]
    player_center = map(lambda x: x / 2, player_images[0].get_rect().size)

    flare_image = pygame.image.load('res/img/shoot_targets/flare.png')
    flare_center = map(lambda x: x / 2, flare_image.get_rect().size)

    def __init__(self, parent, player_num):
        self.parent = parent
        self.image = Player.player_images[player_num]
        self.position = [parent.screen_rect.width * (player_num * 0.8 + 0.1), parent.screen_rect.height / 2]
        self.target_position = self.position[:]
        self.points = 0
        self.direction = [0, 0]
        self.hitbox_radius = 30
        self.flare = False

    def hittest(self, point, radius):
        d = (self.position[0] - point[0]) ** 2 + (self.position[1] - point[1]) ** 2
        return (self.hitbox_radius - radius) ** 2 <= d <= (self.hitbox_radius + radius) ** 2

    def update(self):
        max = self.parent.screen_rect.size
        for i in range(2):
            self.target_position[i] += self.direction[i] * Player.speed

            if self.target_position[i] < 0:
                self.target_position[i] = 0

            if self.target_position[i] > max[i]:
                self.target_position[i] = max[i]

            self.position[i] += (self.target_position[i] - self.position[i]) / Player.damp

        if self.flare:
            for target in self.parent.targets:
                if self.hittest(target.position, target.hitbox_radius):
                    target.hit = True
                    self.points += 1

                    self.parent.sprites.append(ExplosionSprite(self.parent, target.position))

    def render(self):
        if self.flare:
            self.parent.screen.blit(Player.flare_image, map(operator.sub, self.position, Player.flare_center))

        self.parent.screen.blit(self.image, map(operator.sub, self.position, Player.player_center))


