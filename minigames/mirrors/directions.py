import random


class Directions:
    TOP = 180
    RIGHT = 90
    BOTTOM = 0
    LEFT = 270

    @staticmethod
    def random():
        return random.choice([Directions.TOP, Directions.RIGHT, Directions.BOTTOM, Directions.LEFT])