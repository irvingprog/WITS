import pygame
from pygame.sprite import Sprite
import random

class Star(Sprite):
    def __init__(self,difficult):
        Sprite.__init__(self)
        self.difficult = difficult
        if self.difficult == "Easy":
            self.image = pygame.image.load("resources/estrella.png").convert_alpha()
        elif self.difficult == "Medium":
            self.image = pygame.image.load("resources/estrella2.png").convert_alpha()
        elif self.difficult == "Hard":
            self.image = pygame.image.load("resources/estrella3.png").convert_alpha()
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
        if self.calification == 0:
            self.image = pygame.image.load('resources/calificacion0.png').convert_alpha()
        elif self.calification == 1:
            self.image = pygame.image.load('resources/calificacion1.png').convert_alpha()
        elif self.calification == 2:
            self.image = pygame.image.load('resources/calificacion2.png').convert_alpha()        
        elif self.calification == 3:
            self.image = pygame.image.load('resources/calificacion3.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (posx,posy)