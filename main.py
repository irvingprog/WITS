#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame

from pygame.locals import *

from Star import Star, StarsCalification
from Button import Button, ButtonNextLevel
from Text import Text
from Timer import Timer

from CfgUtils import CfgUtils
print "Modules imported"

try:
    import android
    print "android module imported"
except ImportError:
    android = None

scene = None

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("WITS for PC v1.0")
pygame.display.set_icon(pygame.image.load("resources/star.png").convert_alpha())
print "Windows created"

'''
####################################################
#                  SCENES                          #
####################################################
'''     
class Menu():
    def __init__(self):
        self.image = pygame.image.load('resources/background_menu.png').convert()

        self.button_play = Button('resources/button_play.png',SCREEN_WIDTH/2,350)
        #self.button_options = Button('resources/Button1.png',SCREEN_WIDTH/2,425)
        #self.button_credits = Button('resources/Button1.png',SCREEN_WIDTH/2,550)
        #self.button_exit = Button('resources/Button1.png',SCREEN_WIDTH/2,675)

        self.buttons = pygame.sprite.Group()
        self.buttons.add(self.button_play)
        #self.buttons.add(self.button_options)
        #self.buttons.add(self.button_credits)
        #self.buttons.add(self.button_exit)
        
        self.configuration = CfgUtils('configuration.cfg')
        self.language = self.configuration.read('Options', 'language')

        self.font = pygame.font.Font('resources/CrashLandingBB.ttf',170)      

        self.text_play = Text(self.font,self.configuration.read(self.language,'play'),(255,255,255),SCREEN_WIDTH/2,360)
        #self.text_options = Text(self.font,self.configuration.read(self.language,'options'),(255,255,255),512,425)
        #self.text_credits = Text(self.font,self.configuration.read(self.language,'credits'),(255,255,255),512,550)
        #self.text_exit = Text(self.font,self.configuration.read(self.language,'exit'),(255,255,255),512,675)

        print "Menu() created"

    def update(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                exit()
        
            if event.type == MOUSEBUTTONDOWN:
                if self.button_play.rect.collidepoint(event.pos[0],event.pos[1]):
                    difficult_start()
                #if self.button_options.rect.collidepoint(event.pos[0],event.pos[1]):
                    #options_start()
                #if self.button_credits.rect.collidepoint(event.pos[0],event.pos[1]):
                    #print "credits"
                #if self.button_exit.rect.collidepoint(event.pos[0],event.pos[1]):
                    #exit()  

    def draw(self,screen):
        screen.blit(self.image,(0,0))
        self.buttons.draw(screen)
        self.text_play.draw(screen)
        #self.text_options.draw(screen)
        #self.text_credits.draw(screen)
        #self.text_exit.draw(screen)
        pygame.display.flip();

class Difficult():
    def __init__(self):
        self.image = pygame.image.load('resources/background_easy.jpg').convert()

        self.button_easy = Button('resources/Boton_dificultad1.png',512,250)
        self.button_medium = Button('resources/Boton_dificultad2.png',512,375)
        self.button_hard = Button('resources/Boton_dificultad3.png',512,500)

        self.buttons = pygame.sprite.Group()
        self.buttons.add(self.button_easy)
        self.buttons.add(self.button_medium)
        self.buttons.add(self.button_hard)

        self.configuration = CfgUtils('configuration.cfg')
        self.language = self.configuration.read('Options', 'language')

        self.font = pygame.font.Font('resources/ThrowMyHandsUpintheAirBold.ttf',85)    

        self.title = Text(self.font,self.configuration.read(self.language,'dificult'),(255,255,255),512,70)
        self.text_easy = Text(self.font,self.configuration.read(self.language,'easy'),(255,255,255),512,250)
        self.text_medium = Text(self.font,self.configuration.read(self.language,'medium'),(255,255,255),512,375)
        self.text_hard = Text(self.font,self.configuration.read(self.language,'hard'),(255,255,255),512,500)

        print "Difficult() created"

    def update(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if self.button_easy.rect.collidepoint(event.pos[0],event.pos[1]):
                    leveleasy_start()
                if self.button_medium.rect.collidepoint(event.pos[0],event.pos[1]):
                    levelmedium_start()
                if self.button_hard.rect.collidepoint(event.pos[0],event.pos[1]):
                    levelhard_start()

    def draw(self,screen):
        screen.blit(self.image,(0,0))
        self.buttons.draw(screen)
        self.title.draw(screen)
        self.text_easy.draw(screen)
        self.text_medium.draw(screen)
        self.text_hard.draw(screen)
        pygame.display.flip()

class LevelsSelector():
    def __init__(self, continent, difficult):
        self.selector = 0
        self.continent = continent
        self.difficult = difficult

        if self.difficult == "Easy":
            self.image = pygame.image.load('resources/background_easy.jpg').convert()
            self.level_button = 'resources/Boton_nivel1.png'
        elif self.difficult == "Medium":
            self.image = pygame.image.load('resources/background_medium.jpg').convert()
            self.level_button = 'resources/Boton_nivel2.png'
        elif self.difficult == "Hard":
            self.image = pygame.image.load('resources/background_hard.jpg').convert()
            self.level_button = 'resources/Boton_nivel3.png'

        self.levels = []
        self.numbers = []
        self.text_numbers = []
        self.starscalification = []

        self.configuration = CfgUtils('configuration.cfg')
        self.language = self.configuration.read('Options', 'language')

        self.levels_cfg = CfgUtils('levels.cfg')

        self.font = pygame.font.Font('resources/ThrowMyHandsUpintheAirBold.ttf',85)    

        self.buttons_levels = pygame.sprite.Group()
        self.califications_levels = pygame.sprite.Group()

        self.title = Text(self.font,self.configuration.read(self.language,'levels'),(255,255,255),512,70)

        for i in range(0,15):
            self.numbers.append(i+1)
            self.calification_level = self.levels_cfg.read(self.difficult,str(i+1+self.selector))
            if i <5:
                self.levels.append(Button(self.level_button,174+175*i,250))
                self.text_numbers.append(Text(self.font,self.numbers[i]+self.selector,(255,255,255),174+175*i,250))
                self.starscalification.append(StarsCalification(int(self.calification_level),174+175*i,305))
            elif i>=5 and i<10:
                self.levels.append(Button(self.level_button,174+175*i-875,425))
                self.text_numbers.append(Text(self.font,self.numbers[i]+self.selector,(255,255,255),174+175*i-875,425))
                self.starscalification.append(StarsCalification(int(self.calification_level),174+175*i-875,480))
            elif i>=10:
                self.levels.append(Button(self.level_button,174+175*i-1750,+600))
                self.text_numbers.append(Text(self.font,self.numbers[i]+self.selector,(255,255,255),174+175*i-1750,600))
                self.starscalification.append(StarsCalification(int(self.calification_level),174+175*i-1750,655))
            self.buttons_levels.add(self.levels[i])
            self.califications_levels.add(self.starscalification[i])

        print "LevelsSelector() created"

    def update(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                for i in range(0,15):  
                    if self.levels[i].rect.collidepoint(event.pos[0],event.pos[1]):
                        game_start(i+1, self.continent, self.difficult)

    def draw(self,screen):
        screen.blit(self.image,(0,0))
        self.buttons_levels.draw(screen)
        self.califications_levels.draw(screen)
        for i in range(0,15):
            self.text_numbers[i].draw(screen)
        self.title.draw(screen)
        pygame.display.flip()      
        
class WorldSelector():
    def __init__(self, arg):
        pass

class Options():
    def __init__(self):
        self.blanco = (255,255,255)

        self.configuration = CfgUtils('configuration.cfg')
        self.language = self.configuration.read('Options', 'language')

        self.bigfont = pygame.font.Font('resources/ThrowMyHandsUpintheAirBold.ttf',85)
        self.middlefont = pygame.font.Font('resources/ThrowMyHandsUpintheAirBold.ttf',45)

        self.title = Text(self.bigfont,self.configuration.read(self.language,'options'),self.blanco,SCREEN_WIDTH/2,70)
        self.language_text = Text(self.middlefont,self.configuration.read(self.language,'language')+":"+self.configuration.read('Options','language'),self.blanco,200,250)
        self.fullscreen_text = Text(self.middlefont,self.configuration.read(self.language,'fullscreen')+":"+self.configuration.read('Options','fullscreen'),self.blanco,200,350)
        self.sound_text = Text(self.middlefont,self.configuration.read(self.language,'sound')+":"+self.configuration.read('Options','sound'),self.blanco,200,450)

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                exit()
    
    def draw(self,screen):
        screen.fill((0,0,0))
        self.title.draw(screen)
        self.language_text.draw(screen)
        self.fullscreen_text.draw(screen)
        self.sound_text.draw(screen)
        pygame.display.flip()   
        
        
class Game():
    def __init__(self, level, continent, difficult):
        self.level = level
        self.continent = continent
        self.difficult = difficult

        #Configuration Files
        self.configuration = CfgUtils('configuration/configuration.cfg')
        self.language = self.configuration.read('Options', 'language')

        self.rating_level = CfgUtils('configuration/levels_rating.cfg')
        self.current_rating_level = int(self.rating_level.read(self.continent+self.difficult,str(self.level)))

        self.levels_namescfg = CfgUtils('configuration/levels_names.cfg')

        self.path = "resources/levels/"+self.continent+"/"

        self.levels_names = []
        for i in range(1,16): 
            self.levels_names.append(self.levels_namescfg.read(self.continent,"bglevel"+str(self.level)))

        self.color = (0,0,0)
        
        #Level Creator
        for Level in range(1,16):
            if Level==self.level:
                self.image = pygame.image.load(self.path+'bglevel'+str(Level)+'.jpg').convert()
                self.name = self.levels_names[Level-1]
        
        self.font = pygame.font.Font('resources/ThrowMyHandsUpintheAirBold.ttf',35)        
        self.level_title = Text(self.font,self.name,self.color,SCREEN_WIDTH/2,30)

        #Timer 
        self.timer = Timer()
        self.timer.start()

        self.star = Star(self.difficult)        
        self.button_nextlevel = ButtonNextLevel()
        self.sprites = pygame.sprite.RenderUpdates()
        self.sprites.add(self.star)
        self.sprites.add(self.button_nextlevel)

        self.posx_text_nextlevel = 1124

        self.title_shadow = pygame.image.load('resources/sombra_titulo_'+self.difficult+'.png').convert_alpha()

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if self.star.rect.collidepoint(event.pos[0],event.pos[1]):
                    if android:
                        android.vibrate(4)
                    self.star.mover = True
                    if self.timer.time()<2:
                        self.rating_level.write(3)
                    elif self.timer.time()>=2 and self.timer.time()<= 4:
                        if self.current_rating_level == 3:
                            pass
                        else:
                            self.rating_level.write(2)
                    elif self.timer.time()> 4:
                        if self.current_rating_level == 2 or self.current_rating_level == 3:
                            pass
                        else:
                            self.rating_level.write(1)
                    self.timer.stop()
                if self.button_nextlevel.rect.collidepoint(event.pos[0],event.pos[1]):
                    game_start(self.level+1, self.continent, self.difficult)
        
        self.star.update()

        if self.star.rect.x >= 1024:
            self.button_nextlevel.move=True
            self.posx_text_nextlevel -= 10
            if self.posx_text_nextlevel<=890:
                self.posx_text_nextlevel = 890

        if self.button_nextlevel.move:
            self.button_nextlevel.update()
            
    def draw(self,screen):
        #self.texto_temporizador para que no de error al draw.
        #self.texto_temporizador = Texto(self.fuente, self.temporizador.time(),self.color,SCREEN_WIDTH/2,60)
        self.text_nextlevel = Text(self.font,self.configuration.read(self.language,'nextlevel'),self.color,self.posx_text_nextlevel,650)

        screen.blit(self.image,(0,0))
        screen.blit(self.title_shadow,(0,0))
        self.level_title.draw(screen)
        #self.texto_temporizador.draw(screen)
        self.sprites.draw(screen)
        self.text_nextlevel.draw(screen)
        pygame.display.flip()

'''
####################################################
#               FUNCTIONS                          #
#              SCENE CHANGES                       #
####################################################
'''
def game_start(level, continent, difficult):
    print "Changed scene to Game()"+"Continent: "+str(continent)+" Level: "+str(level)+" Difficult: "+difficult
    global scene;
    scene = Game(level, continent, difficult)

def options_start():
    print "Changed scene to Options()"
    global scene
    scene = Options()

def difficult_start():
    print "Changed scene to Difficult()"
    global scene
    scene = Difficult()

def leveleasy_start():
    print "Changed scene to LevelsSelector(Easy)"
    global scene
    scene = LevelsSelector("Easy")

def levelmedium_start():
    print "Changed scene to LevelsSelector(Medium)"
    global scene
    scene = LevelsSelector("Medium")  

def levelhard_start():
    print "Changed scene to LevelsSelector(Hard)"
    global scene
    scene = LevelsSelector("Hard")


'''
####################################################
#              MAIN LOOP                           #
####################################################
''' 
def main():
    global scene
    pygame.init()
    
    clock = pygame.time.Clock()

    scene=Game(1, "Africa", "Easy")

    if android:
        android.init()
        android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)

    while True:
        clock.tick()
        #print clock.get_fps()

        if android:
            if android.check_pause():
                android.wait_for_resume()

        scene.update()
        scene.draw(screen)
        
if __name__ == '__main__':
    main()
