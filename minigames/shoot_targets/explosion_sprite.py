import pygame


class ExplosionSprite:

    length = 8
    side = 160
    image = pygame.image.load('res/img/shoot_targets/explosion.png')
    center = map(lambda x: x / 2, image.get_rect().size)
    delay = 4

    def __init__(self, parent, position):
        self.parent = parent
        self.position = [position[0] - 80, position[1] - 80]
        self.index = 0
        self.finished = False
        self.count = ExplosionSprite.delay

    def update(self):
        self.count -= 1

        if self.index + 1 < ExplosionSprite.length:
            if self.count == 0:
                self.index += 1
                self.count = ExplosionSprite.delay
        else:
            self.finished = True

    def render(self):
        rect = (self.index * ExplosionSprite.side, 0, self.side, self.side)
        self.parent.screen.blit(ExplosionSprite.image, self.position, rect)
