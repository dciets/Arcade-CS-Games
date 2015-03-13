from minigames import multiplayer
import pygame
import input_map
from bar import Bar
from ball import Ball
import random

class UltimatePong(multiplayer.Minigame):
    BAR_SPEED = 15
    BALL_X_SPEED = 10
    name = 'Ultimate Pong!'
    max_duration = 10000
    last_direction = -1

    def init(self):
        self.width, self.height = self.screen.get_size()
        bar_width = 0.03 * self.width
        bar_height = 0.3 * self.height
        self.bars = [Bar(0.1 * self.width, (self.height - bar_height) / 2, bar_width, bar_height, self.height, (255, 0, 0)),
                     Bar(0.9 * self.width - bar_width, (self.height - bar_height) / 2, bar_width, bar_height, self.height, (0, 0, 255))]
        self.balls = []
        self.score = [0, 0]
        self.last_spawn_y = 0.1
        for i in range(4 + 2 * self.difficulty):
            self.create_ball()

    def tick(self):
        pygame.event.get()
        for i, bar in enumerate(self.bars):
            keys = input_map.get_player_keys(i)
            if keys[input_map.UP]:
                bar.move(-self.BAR_SPEED)
            elif keys[input_map.DOWN]:
                bar.move(self.BAR_SPEED)

        for i, ball in enumerate(self.balls):
            ball.move()

        # Check collisions
        for ball in self.balls:
            ball.check_ball_collision(self.balls)
        for ball in self.balls:
            ball.check_bar_collision(self.bars)

        # Check goals.
        balls_to_delete = []
        for ball in self.balls:
            if ball.rect.centerx < 0 or ball.rect.centerx > self.width:
                if ball.rect.centerx < 0:
                    self.score[1] += 1
                elif ball.rect.centerx > self.width:
                    self.score[0] += 1
                balls_to_delete.append(ball)

        # Create new balls and delete the old ones.
        for i in range(len(balls_to_delete)):
            self.create_ball()
        for ball in balls_to_delete:
            self.balls.remove(ball)

        # Draw game.
        self.screen.fill((0, 0, 0))
        for bar in self.bars:
            bar.draw(self.screen)

        for ball in self.balls:
            ball.draw(self.screen)

    def create_ball(self):
        ball_width = ball_height = self.width * 0.05
        x = (self.width - ball_width) / 2
        self.last_spawn_y += 0.1
        if self.last_spawn_y > 0.9:
            self.last_spawn_y = 0
        y = self.last_spawn_y * self.height

        ball = Ball(x, y, self.BALL_X_SPEED * self.last_direction, random.randint(-10, 10), self.width, self.height)
        self.balls.append(ball)
        self.last_direction = -self.last_direction

    def get_results(self):
        if self.score[0] == 0 and self.score[1] == 0:
            return [False, False]
        elif self.score[0] > self.score[1]:
            return [True, False]
        elif self.score[0] < self.score[1]:
            return [False, True]
        else:
            return [True, True]

