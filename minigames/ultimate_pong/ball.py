import pygame
import random


class Ball:
    image = None

    def __init__(self, x, y, speed_x, speed_y, max_width, max_height):
        if Ball.image is None:
            Ball.image = pygame.image.load("res/img/ultimate_pong/ball.png").convert_alpha()
        width, height = Ball.image.get_size()
        self.rect = pygame.Rect(x, y, width, height)
        self.radius = width / 2.0
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.max_width = max_width
        self.max_height = max_height
        self.last_rect = self.rect

    def move(self):
        rect = self.rect.move(self.speed_x, self.speed_y)
        if rect.top < 0:
            rect.move(0, -rect.top)
            self.speed_y = -self.speed_y
        elif rect.bottom > self.max_height:
            rect.move(0, self.max_height - rect.bottom)
            self.speed_y = -self.speed_y

        self.last_rect = self.rect
        self.rect = rect

    def cancel_move(self):
        self.rect = self.last_rect

    def check_ball_collision(self, balls):
        # C'est pas optimise pis j'm'en fous.
        for b in balls:
            if self == b:
                continue

            if abs(self.rect.centerx - b.rect.centerx) < self.radius and abs(self.rect.centery - b.rect.centery) < self.radius:
                self.cancel_move()
                b.cancel_move()
                if random.randint(0, 1) == 0:
                    self.speed_x = -self.speed_x
                    self.speed_y = -self.speed_y
                else:
                    b.speed_x = -b.speed_x
                    b.speed_y = -b.speed_y

                # Hack cheap pour eviter que les balles restent prises entre elles.
                if abs(self.rect.centerx - b.rect.centerx) < self.radius or abs(self.rect.centery - b.rect.centery) < self.radius:
                    self.rect = self.rect.move(self.speed_x, self.speed_y)

    def check_bar_collision(self, bars):
        for b in bars:
            if self.rect.colliderect(b.rect):
                self.cancel_move()
                self.speed_x = -self.speed_x
                self.move()

            # Hack cheap pour pas que les balles restent dans la barre.
            while self.rect.colliderect(b.rect):
                self.move()

    def draw(self, screen):
        screen.blit(Ball.image, (self.rect.x, self.rect.y))
