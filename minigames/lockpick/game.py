import pygame
from minigames import multiplayer
from input_map import *
from random import randint
import math

class Lockpick(multiplayer.Minigame):
	name = "Crack the code!"
	max_duration = 8000

	# CONFIG
	BASE_SPEED = 5
	INCREMENT_SPEED = 5
	HANDLE_SIZE = (20, 100)
	NEAR_SPOT = 80
	SWEET_SPOT = 20
	FAR_COLOR = (200, 0, 0)
	NEAR_COLOR = (255, 255, 0)
	SWEET_COLOR = (0, 180, 0)
	OPEN_ANIM_DURATION = 5

	# SPRITES
	wheel = pygame.image.load("./res/img/lockpick/wheel.png")

	def __init__(self, game):
		multiplayer.Minigame.__init__(self, game)
		self.width = game.GAME_WIDTH
		self.height = game.GAME_HEIGHT

		# Initialize game state
		self.speed = self.BASE_SPEED + self.INCREMENT_SPEED * self.difficulty
		self.score = [0, 0]
		self.positions = [0, 0]
		self.velocities = [0, 0]
		self.target = [randint(0, 359), randint(0, 359)]

		# Initialize anim state
		self.open_anim_position = [-1, -1]

	def tick(self):
		self.update()
		self.draw()

	def update(self):
		# Listen for inputs
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				for i in range(2):
					if event.key == PLAYERS_MAPPING[i][LEFT]:
						self.velocities[i] = -self.speed
					elif event.key == PLAYERS_MAPPING[i][RIGHT]:
						self.velocities[i] = self.speed
					elif event.key == PLAYERS_MAPPING[i][ACTION]:
						self.openSafe(i)
			elif event.type == KEYUP:
				for i in range(2):
					if (event.key == PLAYERS_MAPPING[i][LEFT]) or \
						(event.key == PLAYERS_MAPPING[i][RIGHT]):
						self.velocities[i] = 0

		# Apply velocities
		for i in range(2):
			self.positions[i] = (self.positions[i] + self.velocities[i]) % 360

		# Update anim positions
		for i in range(2):
			if self.open_anim_position[i] >= 0:
				self.open_anim_position[i] += 1
			if self.open_anim_position[i] > self.OPEN_ANIM_DURATION:
				self.open_anim_position[i] = -1

	def draw(self):
		self.screen.fill((0, 0, 0))

		for i in range(2):
			playerWCenter = self.width * (0.5*i + 0.25)
			playerHCenter = self.height * 0.5

			# Draw the arrow
			arrowPoints = self.get_arrow_points(i)

			pygame.draw.polygon( \
				self.screen, \
				self.get_arrow_color(self.positions[i], self.target[i]), \
				arrowPoints, 0 \
			)

			# Draw the wheel
			playerWheel = rot_center(self.wheel, self.positions[i])
			self.screen.blit(\
				playerWheel, \
				[ \
					playerWCenter - self.wheel.get_width()/2, \
					playerHCenter - self.wheel.get_height()/2 \
				] \
			)

	def openSafe(self, player):
		if (abs(self.positions[player] - self.target[player]) < self.SWEET_SPOT):
			self.score[player] += 1
		else:
			self.score[player] -= 1
			if self.score[player] < 0:
				self.score[player] = 0

		self.target[player] = randint(0, 359)
		self.open_anim_position[player] = 0 # Start open safe anim

	def get_arrow_color(self, pos, target):
		diffs = (abs(pos - target), abs((pos+360) - target), abs(pos - (360+target)))

		for diff in diffs:
			if diff < self.SWEET_SPOT:
				return self.SWEET_COLOR
		for diff in diffs:
			if (diff < self.NEAR_SPOT):
				return self.NEAR_COLOR

		return self.FAR_COLOR

	def get_results(self):
		return [self.score[0] >= self.score[1], self.score[0] <= self.score[1]]

	def get_arrow_points(self, player):
		playerWCenter = self.width * (0.5*player + 0.25)
		playerHCenter = self.height * 0.5
		animOffset = opensafe_anim_curve(float(self.open_anim_position[player]) / float(self.OPEN_ANIM_DURATION))

		return ( \
			(playerWCenter - 10, playerHCenter - 160 + animOffset), \
			(playerWCenter + 10, playerHCenter - 160 + animOffset), \
			(playerWCenter, playerHCenter - 120 + animOffset) \
		)

def rot_center(image, angle):
    """rotate an image while keeping its center and size http://pygame.org/wiki/RotateCenter"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def opensafe_anim_curve(x):
	return 20 * math.sin(x * math.pi)
