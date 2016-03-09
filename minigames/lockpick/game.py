import pygame
from minigames import multiplayer
from input_map import *
from random import randint
import math

class Lockpick(multiplayer.Minigame):
    name = "Open the lock!"

    # CONFIG
    FINISHED = {'NOT': -1, 'PASS': 0, 'FAIL': 1}
    BASE_SPEED = 5
    INCREMENT_SPEED = 4
    HANDLE_SIZE = (20, 100)
    SWEET_SPOT = 20
    FAR_COLOR = (200, 0, 0)
    SWEET_COLOR = (0, 180, 0)
    OPEN_ANIM_DURATION = 5

    # SPRITES
    wheel = pygame.image.load("./res/img/lockpick/wheel.png")
    passMark = pygame.image.load("./res/img/lockpick/pass.png")
    failMark = pygame.image.load("./res/img/lockpick/fail.png")

    def __init__(self, game):
        multiplayer.Minigame.__init__(self, game)
        self.width = game.GAME_WIDTH
        self.height = game.GAME_HEIGHT

        # Initialize difficulty
        self.max_duration = 8000 - self.difficulty * 500
        self.speed = self.BASE_SPEED + self.INCREMENT_SPEED * self.difficulty

        # Initialize game state
        self.score = [0, 0]
        self.finished = [self.FINISHED['NOT'], self.FINISHED['NOT']]
        self.positions = [0, 0]
        self.velocities = [0, 0]

        self.target_bank = []
        target = 0
        last_target = 0
        for i in range(3):
            while (abs(last_target - target) < 45):
                target = randint(0, 359)

            self.target_bank.append(target)
            last_target = target

        self.target = [self.target_bank[0], self.target_bank[0]]

        # Initialize anim state
        self.open_anim_position = [-1, -1]

    def tick(self):
        self.update()
        self.draw()

    def update(self):
        # Listen for inputs
        for event in pygame.event.get():
            for i in range(2):
                if (self.finished[i] == self.FINISHED['NOT']):
                    if event.type == KEYDOWN:
                        if event.key == PLAYERS_MAPPING[i][LEFT]:
                            self.velocities[i] = -self.speed
                        elif event.key == PLAYERS_MAPPING[i][RIGHT]:
                            self.velocities[i] = self.speed
                        if event.key == PLAYERS_MAPPING[i][ACTION]:
                            self.open_safe(i)

                    elif event.type == KEYUP:
                        if (event.key == PLAYERS_MAPPING[i][LEFT]) or \
                            (event.key == PLAYERS_MAPPING[i][RIGHT]):
                            self.velocities[i] = 0

        for i in range(2):
            if (self.finished[i] == self.FINISHED['NOT']):
                # Apply velocities
                self.positions[i] = (self.positions[i] + self.velocities[i]) % 360

                # Update anim positions
                if self.open_anim_position[i] >= 0:
                    self.open_anim_position[i] += 1
                if self.open_anim_position[i] > self.OPEN_ANIM_DURATION:
                    self.open_anim_position[i] = -1

    def draw(self):
        self.screen.fill((0, 0, 0))

        for i in range(2):
            playerWCenter = self.width * (0.5*i + 0.25)
            playerHCenter = self.height * 0.5

            # Draw the wheel
            playerWheel = rot_center(self.wheel, self.positions[i])
            self.screen.blit( \
                playerWheel, \
                [ \
                    playerWCenter - self.wheel.get_width()/2, \
                    playerHCenter - self.wheel.get_height()/2 \
                ] \
            )

            if (self.finished[i] == self.FINISHED['NOT']):
                # Draw the arrow
                arrowPoints = self.get_arrow_points(i)

                pygame.draw.polygon( \
                    self.screen, \
                    self.get_arrow_color(self.positions[i], self.target[i]), \
                    arrowPoints, 0 \
                )

                # Draw the target arc
                arcRect = pygame.Rect( \
                    playerWCenter - self.wheel.get_width()/2 + 15, \
                    playerHCenter - self.wheel.get_height()/2 + 15, \
                    self.wheel.get_width() - 30, \
                    self.wheel.get_height() - 30 \
                )

                pygame.draw.arc( \
                    self.screen, \
                    self.SWEET_COLOR, \
                    arcRect, \
                    deg_to_rad(self.positions[i] - self.target[i] - self.SWEET_SPOT + 90), \
                    deg_to_rad(self.positions[i] - self.target[i] + self.SWEET_SPOT + 90), \
                    10 \
                )

                # Draw the lock lights
                for j in range(3):
                    pygame.draw.circle( \
                        self.screen, \
                        self.get_lock_light_color(i, j), \
                        [int(playerWCenter - 20 + 20*j), int(playerHCenter)], \
                        8 \
                    )

            # Draw the finished mark
            markPos = [int(playerWCenter - self.passMark.get_width()/2), playerHCenter + 150]
            if (self.finished[i] == self.FINISHED['PASS']):
                self.screen.blit(self.passMark, markPos)
            elif (self.finished[i] == self.FINISHED['FAIL']):
                self.screen.blit(self.failMark, markPos)

    def open_safe(self, player):
        distToTarget = abs(self.positions[player] - self.target[player])
        if (distToTarget < self.SWEET_SPOT or distToTarget > 360 - self.SWEET_SPOT):
            self.score[player] += 1
            if self.score[player] == 3:
                self.finished[player] = self.FINISHED['PASS']
        else:
            self.finished[player] = self.FINISHED['FAIL']

        if self.finished[player] == self.FINISHED['NOT']:
            self.target[player] = self.target_bank[self.score[player]]
            self.open_anim_position[player] = 0 # Start open safe anim

    def get_arrow_color(self, pos, target):
        diffs = (abs(pos - target), abs((pos+360) - target), abs(pos - (360+target)))

        for diff in diffs:
            if diff < self.SWEET_SPOT:
                return self.SWEET_COLOR

        return self.FAR_COLOR

    def get_results(self):
        return [self.score[0] >= 3, self.score[1] >= 3]

    def get_arrow_points(self, player):
        '''
        Returns the points for the arrow poly for a given `player` according to the arrow animation
        '''
        playerWCenter = self.width * (0.5*player + 0.25)
        playerHCenter = self.height * 0.5
        animOffset = open_safe_anim_curve(float(self.open_anim_position[player]) / float(self.OPEN_ANIM_DURATION))

        return ( \
            (playerWCenter - 10, playerHCenter - 160 + animOffset), \
            (playerWCenter + 10, playerHCenter - 160 + animOffset), \
            (playerWCenter, playerHCenter - 120 + animOffset) \
        )

    def get_lock_light_color(self, player, light):
        '''
        Returns the color of the `light`nth light of a given `player`
        '''
        if (self.score[player] > light):
            return self.SWEET_COLOR
        else:
            return self.FAR_COLOR

def rot_center(image, angle):
    '''
    Rotate an `image` surface `angle` degrees while keeping its center and size
    @see http://pygame.org/wiki/RotateCente
    '''
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def open_safe_anim_curve(x):
    return 20 * math.sin(x * math.pi)

def deg_to_rad(deg):
    return float(deg / 180.0 * math.pi)
