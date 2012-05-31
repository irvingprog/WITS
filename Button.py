import pygame
from pygame.sprite import Sprite
	
class Button(Sprite):
	def __init__(self,image,posx,posy):
		Sprite.__init__(self)
		self.image = pygame.image.load(image).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = (posx,posy)

class ButtonNextLevel(Sprite):
	def __init__(self):
		Sprite.__init__(self)
		self.image = pygame.image.load("resources/siguientenivel.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.height = 75
		self.rect.x = 1024
		self.rect.y = 620

		self.move = False

	def update(self):
		if self.move:
			self.rect.x -= 10
			if self.rect.x<=784:
				self.rect.x = 784
           