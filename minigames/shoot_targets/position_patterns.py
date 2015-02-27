import random
import math
import operator
from target import Target


target_rect = Target.image.get_rect()


def sin_pattern(game):
    targets = []
    width, height = game.screen_rect.size

    n = width / target_rect.width - 2
    a = math.pi * 2 / n
    margin = target_rect.width
    top = height * 0.5
    dy = height * 0.35
    r0 = random.random() * math.pi * 2

    for i in range(n):
        y = top + math.sin(r0 + a * i) * dy
        targets.append(Target(game, [margin + 45 * i, y]))

    return targets


def ellipse_pattern(game):
    targets = []
    width, height = game.screen_rect.size

    cx, cy = width / 2, height / 2
    n = 20
    a = math.pi * 2 / n
    r = 0
    w = random.randrange(width * 0.15, width * 0.4)
    h = random.randrange(height * 0.15, height * 0.4)

    for i in range(n):
        x, y = cx + math.cos(r) * w, cy + math.sin(r) * h
        targets.append(Target(game, [x, y]))
        r += a

    return targets


def grid_pattern(game):
    targets = []
    width, height = game.screen_rect.size

    tx, ty = target_rect.width * 1.1, target_rect.height * 1.1
    nx, ny = int(width / tx - 2), int(height / ty - 2)
    k = random.randint(1, 3)
    op = random.choice([operator.mul, operator.add])

    mx = ((nx * tx - tx) - width) / 2
    my = ((ny * ty - ty) - height) / 2

    for i in range(nx):
        for j in range(ny):
            if op(i, j) % k == 0:
                targets.append(Target(game, [tx * i - mx, ty * j - my]))

    return targets


patterns = [
    # sin_pattern,
    ellipse_pattern,
    grid_pattern
]


def generate_targets(game):
    return random.choice(patterns)(game)