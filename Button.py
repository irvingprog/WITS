import pygame
from pygame.sprite import Sprite
	
class Button(Sprite):
	def __init__(self,image,posx,posy):
		Sprite.__init__(self)
		self.image = pygame.image.load(image).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = (posx,posy)
