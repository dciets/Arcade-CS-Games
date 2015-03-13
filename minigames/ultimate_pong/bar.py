import pygame


class Bar:
    def __init__(self, x, y, width, height, game_height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.game_height = game_height
        self.color = color
        
    def move(self, speed):
        rect = self.rect.move(0, speed)
        if rect.top < 0:
            rect = rect.move(0, -rect.top)
        if rect.bottom > self.game_height:
            rect = rect.move(0, self.game_height - rect.bottom)
        self.rect = rect

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
 