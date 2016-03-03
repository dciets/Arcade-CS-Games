import pygame
from minigames import multiplayer
from input_map import *

class Lockpick(multiplayer.Minigame):
	name = "Crack the code!"
	duration = 5

	# CONFIG
	SPEED = 20
	HANDLE_SIZE = [20, 100]
	width, height = 0, 0

	# GAME STATE
	scores = [0, 0]
	velocities = [0, 0]
	positions = [0, 0]

	# SPRITES
	handles = []

	def __init__(self, game):
		multiplayer.Minigame.__init__(self, game)
		self.width = game.GAME_WIDTH
		self.height = game.GAME_HEIGHT

		self.scores = [0, 0]
		self.positions = [0, 0]
		self.velocities = [0, 0]

		for i in range(2):
			self.handles.append( \
				pygame.Rect(self.width * (0.5*i + 0.25), self.height * 0.5, \
				self.HANDLE_SIZE[0], self.HANDLE_SIZE[1]) \
			)

	def tick(self):
		self.update()
		self.draw()

	def update(self):
		# Listen for inputs
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				for i in range(2):
					if event.key == PLAYERS_MAPPING[i][LEFT]:
						self.velocities[i] = -self.SPEED
					elif event.key == PLAYERS_MAPPING[i][RIGHT]:
						self.velocities[i] = self.SPEED
					elif event.key == PLAYERS_MAPPING[i][ACTION]:
						self.open(i)
			elif event.type == KEYUP:
				for i in range(2):
					if (event.key == PLAYERS_MAPPING[i][LEFT]) or \
						(event.key == PLAYERS_MAPPING[i][RIGHT]):
						self.velocities[i] = 0

		# Apply velocities
		for i in range(2):
			self.positions[i] = (self.positions[i] + self.velocities[i]) % 360

	def draw(self):
		print "Player positions: [" + str(self.positions[0]) + ", " + str(self.positions[1]) + "]"
		self.screen.fill((0, 0, 0))

		for handle in self.handles:
			pygame.draw.rect(self.screen, (255, 255, 255), handle)

	def open(self, player):
		print "player " + str(player) + " opens the safe"

	def get_results(self):
		if self.scores[0] > self.scores[1]:
			return [True, False]
		elif self.scores[0] < self.scores[1]:
			return [False, True]
		else:
			return [True, True]
