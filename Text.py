import pygame
from pygame.sprite import Sprite

class Text(Sprite):
	"""docstring for Texto"""
	def __init__(self, font, text, color, x, y):
		Sprite.__init__(self)
		self.font = font
		self.text = text
		self.color = color
		self.x = x
		self.y = y

		self.__create()

	def __create(self):
		self.image = self.font.render(str(self.text),1,self.color)
		self.rect = self.image.get_rect()
		self.rect.center = (self.x,self.y)

	def draw(self,screen):
		screen.blit(self.image,self.rect)

		