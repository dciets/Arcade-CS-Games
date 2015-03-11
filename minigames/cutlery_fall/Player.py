import pygame

class Player:
    def __init__(self):
        self.FREEZE_TIME = 1.0
        self.freeze = False
        self.score = 0
        self.timeFreeze = 0

    def update(self, elapsed):
        if self.freeze:
            if self.timeFreeze >= self.FREEZE_TIME:
                self.timeFreeze = 0
                self.freeze = False
            else:
                self.timeFreeze += elapsed
