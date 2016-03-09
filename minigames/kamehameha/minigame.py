import math
import pygame
from input_map import *
from minigames import minigame
from minigames.kamehameha.entities.character import Character

# Image credit: Calmune, Bonzai, Son Goharotto, Angry Boy, LSWA, Debons, Hitsugaya

def midX(rect):
	return rect[0] + rect[2] / 2

class KamehamehaMinigame(minigame.Minigame):
	name = "KAMEHAMEHA!"
	game_type = minigame.MULTIPLAYER
	max_duration = 30000
	
	def __init__(self, game):
		minigame.Minigame.__init__(self, game)
		self.beamPower = 0
	
	def init(self):
		self.left = Character(self, "left")
		self.right = Character(self, "right")
		self.background = self.load("background.png")
	
	def load(self, filename):
		im = pygame.image.load("minigames/kamehameha/images/%s" % filename)
		width, height = im.get_size()
		return pygame.transform.scale(im, (width * 3, height * 3))
	
	def align(self, image, hAnchor, vAnchor):
		iWidth, iHeight = image.get_size()
		
		sWidth, sHeight = self.screen.get_size()
		sBoxXOrigin = 8
		sBoxWidth = sWidth - sBoxXOrigin * 2
		
		iX = sBoxXOrigin + (sBoxWidth - iWidth) * hAnchor
		iY = (sHeight - iHeight) * vAnchor
		return (iX, iY, iWidth, iHeight)
	
	def tick(self):
		self.update()
		self.draw()
	
	def update(self):
		multipliers = [1, -1]
		buttons = [x[ACTION] for x in PLAYERS_MAPPING]
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				for i in range(2):
					if event.key == buttons[i]:
						self.beamPower += self.frame * multipliers[i] * 3 / 4
						break
	
	def draw(self):
		left = self.left.image()
		leftRect = self.align(left, 0, 0.5)
		right = self.right.image()
		rightRect = self.align(right, 1, 0.5)
		
		beam0Source = self.left.beam_start()
		beam0SourceRect = (leftRect[0] + leftRect[2], leftRect[1]) + beam0Source.get_size()
		
		beam1Source = self.right.beam_start()
		beam1SourceSize = beam1Source.get_size()
		beam1SourceRect = (rightRect[0] - beam1SourceSize[0], rightRect[1]) + beam1SourceSize
		
		beamMinX = midX(leftRect)
		beamMaxX = midX(rightRect)
		beamMeetpoint = int(((self.beamPower + 1000) / 2000.) * (beamMaxX - beamMinX) + beamMinX)
		
		beam0End = self.left.beam_tip()
		beam0EndSize = beam0End.get_size()
		beam0EndRect = (beamMeetpoint - beam0EndSize[0], leftRect[1]) + beam0EndSize
		
		beam1End = self.right.beam_tip()
		beam1EndRect = (beamMeetpoint, rightRect[1]) + beam1End.get_size()
		
		beam0SectionRect = (midX(beam0SourceRect), beam0SourceRect[1])
		beam0SectionRect += (midX(beam0EndRect) - beam0SectionRect[0], beam0SourceRect[3])
		
		beam1SectionRect = (midX(beam1EndRect), beam1EndRect[1])
		beam1SectionRect += (midX(beam1SourceRect) - beam1SectionRect[0], beam1SourceRect[3])
		
		i = min(1000, abs(self.beamPower)) / 1000.
		ii = 1 - i
		baseColor = (0xe5, 0xaa, 0xdc) if self.beamPower < 0 else (0x93, 0xcd, 0xfb)
		color = [i * c + ii * 0xff for c in baseColor]
		
		self.screen.fill(color)
		
		curveCoeff = KamehamehaMinigame.max_duration / float(self.frame + 1) + 1
		bgOffset = (self.frame * min(15, math.sqrt(curveCoeff))) % 60 - 60
		self.screen.blit(self.background, (0, bgOffset))
		
		self.screen.blit(left, leftRect)
		self.screen.blit(right, rightRect)
		
		if beam0SectionRect[2] > 0:
			self.screen.blit(self.left.beam_mid(beam0SectionRect[2]), beam0SectionRect)
		
		if beam1SectionRect[2] > 0:
			self.screen.blit(self.right.beam_mid(beam1SectionRect[2]), beam1SectionRect)
		
		if beam0SourceRect[0] < beam0EndRect[0]:
			self.screen.blit(beam0Source, beam0SourceRect)
		
		if beam1SourceRect[0] > beam1EndRect[0]:
			self.screen.blit(beam1Source, beam1SourceRect)
		
		self.screen.blit(beam0End, beam0EndRect)
		self.screen.blit(beam1End, beam1EndRect)
	
	def get_duration(self):
		return self.elapsed_ms if abs(self.beamPower) >= 1000 else KamehamehaMinigame.max_duration
	
	def get_results(self):
		return (self.beamPower > 0, self.beamPower < 0)
