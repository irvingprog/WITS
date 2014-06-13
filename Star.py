import pygame
from pygame.sprite import Sprite
import random


class Star(Sprite):
    def __init__(self,difficult):
        Sprite.__init__(self)
        self.difficult = difficult
        self.image = pygame.image.load('resources/star_'+self.difficult+'.png').convert_alpha()
        self.image_move = pygame.image.load('resources/star.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.width = 80
        self.rect.height = 80
        self.rect.x = random.randint(0,950)
        self.rect.y = random.randint(50,650)

        self.x = self.rect.x
        self.y = self.rect.y

        self.move = False

    def change_state(self):
        self.move = True
        self.image = self.image_move

class StarsCalification(Sprite):
    def __init__(self,calification,posx,posy):
        Sprite.__init__(self)
        self.calification = calification
        self.image = pygame.image.load('resources/calificacion'+str(self.calification)+'.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (posx,posy)

class StarMove(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.image.load('resources/star.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(600,1450)
        self.rect.y = random.randint(-400,-10)
        self.speed = random.randint(5,15)

    def update(self):
        self.rect.x -= self.speed
        self.rect.y += self.speed

        if self.rect.x < 0:
            self.rect.x = random.randint(600,1450)
            self.rect.y = random.randint(-400,-10)

class ObjectMoveGoal(Sprite):
    def __init__(self,image,x,y):
        Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.x = x
        self.y = y

        self.state = False

        