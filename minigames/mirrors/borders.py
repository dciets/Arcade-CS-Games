import random


class Borders:
    TOP = 180
    RIGHT = 90
    BOTTOM = 0
    LEFT = 270

    @staticmethod
    def random():
        return random.choice([Borders.TOP, Borders.RIGHT, Borders.BOTTOM, Borders.LEFT])