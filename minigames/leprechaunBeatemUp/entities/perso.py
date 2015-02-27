from sprite import Sprite

class Perso:
    def __init__(self, x, y, path, difficulty):
        self.HIT_DURATION = 0.8
        self.HURT_DURATION = 0.8
        self.HURT_POWER = 300
        self.hitTime = 0
        self.hurtTime = 0

        self.state = "normal"
        self.sprite = Sprite(path)

        self.pos = [x,y]
        self.speed = difficulty * 0.5 + 2
        self.money = 0

        self.pushedVector = [0,0]

    def update(self, timeElapsed):
        if self.state == "hit":
            self.hitTime += timeElapsed
            if self.hitTime >= self.HIT_DURATION:
                self.normal()
                self.hitTime = 0
        if self.state == "hurt":
            self.hurtTime += timeElapsed
            if self.hurtTime >= self.HURT_DURATION:
                self.normal()
                self.hurtTime = 0

        self.updatePos(timeElapsed)
        self.sprite.update(timeElapsed)

    def updatePos(self, timeElapsed):
        if self.pos[0] < 0:
            self.pos[0] = 0
            self.pushedVector[0] = -self.pushedVector[0]
        elif self.pos[0] > 800:
            self.pos[0] = 800
            self.pushedVector[0] = -self.pushedVector[0]
        if self.pos[1] < 200:
            self.pos[1] = 200
            self.pushedVector[1] = -self.pushedVector[1]
        elif self.pos[1] > 600:
            self.pos[1] = 600
            self.pushedVector[1] = -self.pushedVector[1]

        self.pos[0] = self.pos[0] + self.pushedVector[0] * timeElapsed / self.HURT_DURATION
        self.pos[1] = self.pos[1] + self.pushedVector[1] * timeElapsed / self.HURT_DURATION
        self.pushedVector[0] = self.pushedVector[0] - self.pushedVector[0] * timeElapsed / self.HURT_DURATION
        self.pushedVector[1] = self.pushedVector[1] - self.pushedVector[1] * timeElapsed / self.HURT_DURATION

    def draw(self, screen):
        self.sprite.draw(screen, self.pos)

    def move(self, direction):
        if direction == "up":
            self.pos[1] -= self.speed
        elif direction == "left":
            self.pos[0] -= self.speed
        elif direction == "right":
            self.pos[0] += self.speed
        elif direction == "down":
            self.pos[1] += self.speed

        if self.state != "hit" and self.state != "hurt":
            self.sprite.changeSprite(direction)

    def normal(self):
        self.state = "normal"
        self.sprite.changeSprite("normal")

    def hit(self):
        if self.state != "hit" and self.state != "hurt":
            self.state = "hit"
            self.sprite.changeSprite("action")

            return True
        else:
            return False

    def isHurt(self):
        return self.state == "hurt"
    
    def hurt(self, pos):
        newPos = [self.pos[0] - pos[0], self.pos[1] - pos[1]]
        max = abs(newPos[0]) if (abs(newPos[0]) > abs(newPos[1])) else abs(newPos[1])
        self.pushedVector = [self.HURT_POWER * newPos[0] / max, self.HURT_POWER * newPos[1] / max]
        self.state = "hurt"
        self.sprite.changeSprite("action")
