import pygame
from pygame.sprite import Sprite
import random

class Star(Sprite):
    def __init__(self,difficult):
        Sprite.__init__(self)
        self.difficult = difficult
        self.image = pygame.image.load('resources/estrella_'+self.difficult+'.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.width = 80
        self.rect.height = 80
        self.rect.x = random.randint(0,950)
        self.rect.y = random.randint(50,650)
        
        self.mover = False

    def update(self):
        if self.mover:
            self.rect.x += 35

class StarsCalification(Sprite):
    """docstring for EstrellasCalification"""
    def __init__(self,calification,posx,posy):
        Sprite.__init__(self)
        self.calification = calification
        self.image = pygame.image.load('resources/calificacion'+str(self.calification)+'.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (posx,posy)