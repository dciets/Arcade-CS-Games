import pygame

class Character:
	def __init__(self, game, name):
		self.game = game
		self.sprite = game.load("%s-0.png" % name)
		self.beam = [
			game.load("%s-b0.png" % name),
			game.load("%s-b1.png" % name),
			game.load("%s-b2.png" % name),
		]
	
	def image(self):
		return self.sprite
	
	def beam_start(self):
		return self.beam[0]
	
	def beam_mid(self, width):
		return pygame.transform.scale(self.beam[1], (width, self.beam[1].get_size()[1]))
	
	def beam_tip(self):
		return self.beam[2]
