#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

from Star import Star, StarsCalification, StarMove
from Button import Button, ButtonNextLevel
from Text import Text
from Timer import Timer

from CfgUtils import CfgUtils
print "Modules imported"

import os
import platform

os.environ['SDL_VIDEO_CENTERED'] = '1'
if platform.system() == 'Windows':
    os.environ['SDL_VIDEODRIVER'] = 'windib'

try:
    import android
    #import android_mixer
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
        self.background = pygame.image.load('resources/background_menu.png').convert()
        self.logo = pygame.image.load('resources/logo.png').convert_alpha()
        self.shadow_goal = pygame.image.load('resources/shadow_goal.png').convert_alpha()
        self.earth_planet = pygame.image.load('resources/earthplanet.png').convert_alpha()

        #Buttons creation
        self.button_play = Button("resources/button_play.png",SCREEN_WIDTH/2,350)
        self.button_credits = Button("resources/button_credits.png",300,350)
        self.button_exit = Button("resources/button_exit.png",725,350)

        self.buttons = pygame.sprite.Group()
        self.buttons.add(self.button_play)
        self.buttons.add(self.button_credits)
        self.buttons.add(self.button_exit)

        #Stars
        self.stars = pygame.sprite.Group()
        for i in range(10):
            self.stars.add(StarMove())

        #Read configuration
        self.configuration = CfgUtils("configuration/configuration.cfg")
        self.languageID = self.configuration.read('Options','language')
        self.language = CfgUtils("configuration/language.cfg")

        #Fonts
        self.fonts = {
                    'large' : pygame.font.Font("resources/CrashLandingBB.ttf",120), 
                    'middle' : pygame.font.Font("resources/CrashLandingBB.ttf",40),
                    'small' : pygame.font.Font("resources/CrashLandingBB.ttf",35)     
        }

        #Colors
        self.white = (255,255,255)

        self.text_play = Text(self.fonts['large'],self.language.read(self.languageID,'play'),self.white,SCREEN_WIDTH/2,360)
        self.text_credits = Text(self.fonts['middle'],self.language.read(self.languageID,'credits'),self.white,300,450)
        self.text_exit = Text(self.fonts['middle'],self.language.read(self.languageID,'exit'),self.white,725,450)
        self.text_goal = Text(self.fonts['small'],self.language.read(self.languageID,'goal'),self.white,1900,650)

        print "Menu() created"

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                exit()
        
            if event.type == MOUSEBUTTONDOWN:
                if self.button_play.rect.collidepoint(event.pos[0],event.pos[1]):
                    worldselector_start()
                if self.button_credits.rect.collidepoint(event.pos[0],event.pos[1]):
                    credits_start()
                if self.button_exit.rect.collidepoint(event.pos[0],event.pos[1]):
                    exit() 

        self.stars.update()

        self.text_goal.rect.x -= 2.5
        if self.text_goal.rect.x < -1350:
            self.text_goal.rect.x = 1900

    def draw(self,screen):
        screen.blit(self.background,(0,0))
        self.stars.draw(screen)
        screen.blit(self.logo,(280,40))
        screen.blit(self.earth_planet,(176,400))
        self.buttons.draw(screen)
        self.text_play.draw(screen)
        self.text_credits.draw(screen)
        self.text_exit.draw(screen)
        screen.blit(self.shadow_goal,(0,625))
        self.text_goal.draw(screen)
        pygame.display.flip();

class Difficult():
    def __init__(self,continent):
        self.continent = continent
        
        self.background = pygame.image.load('resources/background_difficult.png').convert()
        self.button_return= Button('resources/button_return.png',100,650)

        #Buttons creation
        self.button_easy = Button('resources/Boton_dificultad1.png',512,250)
        self.button_medium = Button('resources/Boton_dificultad2.png',512,375)
        self.button_hard = Button('resources/Boton_dificultad3.png',512,500)

        self.buttons = pygame.sprite.Group()
        self.buttons.add(self.button_easy)
        self.buttons.add(self.button_medium)
        self.buttons.add(self.button_hard)
        self.buttons.add(self.button_return)

        #Read configuration
        self.configuration = CfgUtils('configuration/configuration.cfg')
        self.languageID = self.configuration.read('Options','language')
        self.language = CfgUtils('configuration/language.cfg')

        #Fonts
        self.fonts = {
                    'large' : pygame.font.Font('resources/CrashLandingBB.ttf',170), 
                    'medium' : pygame.font.Font('resources/ThrowMyHandsUpintheAirBold.ttf',85),
        }    

        #Colors
        self.white = (255,255,255)

        self.title = Text(self.fonts['large'],self.language.read(self.languageID,'dificult'),self.white,512,70)
        self.text_easy = Text(self.fonts['medium'],self.language.read(self.languageID,'easy'),self.white,512,250)
        self.text_medium = Text(self.fonts['medium'],self.language.read(self.languageID,'medium'),self.white,512,375)
        self.text_hard = Text(self.fonts['medium'],self.language.read(self.languageID,'hard'),self.white,512,500)

        print "Difficult() created"

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if self.button_easy.rect.collidepoint(event.pos[0],event.pos[1]):
                    levelsselector_start(self.continent,"Easy")
                if self.button_medium.rect.collidepoint(event.pos[0],event.pos[1]):
                    levelsselector_start(self.continent,"Medium")
                if self.button_hard.rect.collidepoint(event.pos[0],event.pos[1]):
                    levelsselector_start(self.continent,"Hard")
                if self.button_return.rect.collidepoint(event.pos[0],event.pos[1]):
                    worldselector_start()

    def draw(self,screen):
        screen.blit(self.background,(0,0))
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

        self.background = pygame.image.load('resources/background_'+self.difficult+'.jpg').convert()
        self.button_return= Button('resources/button_return.png',100,100)        

        self.levels = []
        self.numbers = []
        self.text_numbers = []
        self.starscalification = []

        #Read configuration
        self.configuration = CfgUtils('configuration/configuration.cfg')
        self.languageID = self.configuration.read('Options','language')
        self.language = CfgUtils('configuration/language.cfg')

        self.levels_cfg = CfgUtils('configuration/levels_rating.cfg')

        #Fonts
        self.fonts = {
                    'large' : pygame.font.Font('resources/CrashLandingBB.ttf',170), 
                    'medium' : pygame.font.Font('resources/ThrowMyHandsUpintheAirBold.ttf',85),
        }  

        #Colors
        self.white = (255,255,255)

        self.buttons_levels = pygame.sprite.Group()
        self.buttons_levels.add(self.button_return)
        self.califications_levels = pygame.sprite.Group()

        self.title = Text(self.fonts['large'],self.language.read(self.languageID,'levels'),self.white,512,70)

        #Buttons creation
        for i in range(0,15):
            self.numbers.append(i+1)
            self.calification_level = self.levels_cfg.read(self.continent+self.difficult,str(i+1+self.selector))
            if i <5:
                self.levels.append(Button('resources/button_'+self.difficult+'.png',174+175*i,250))
                self.text_numbers.append(Text(self.fonts['medium'],self.numbers[i]+self.selector,self.white,174+175*i,250))
                self.starscalification.append(StarsCalification(int(self.calification_level),174+175*i,305))
            elif i>=5 and i<10:
                self.levels.append(Button('resources/button_'+self.difficult+'.png',174+175*i-875,425))
                self.text_numbers.append(Text(self.fonts['medium'],self.numbers[i]+self.selector,self.white,174+175*i-875,425))
                self.starscalification.append(StarsCalification(int(self.calification_level),174+175*i-875,480))
            elif i>=10:
                self.levels.append(Button('resources/button_'+self.difficult+'.png',174+175*i-1750,+600))
                self.text_numbers.append(Text(self.fonts['medium'],self.numbers[i]+self.selector,self.white,174+175*i-1750,600))
                self.starscalification.append(StarsCalification(int(self.calification_level),174+175*i-1750,655))
            self.buttons_levels.add(self.levels[i])
            self.califications_levels.add(self.starscalification[i])

        print "LevelsSelector() created"

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                for i in range(0,15):  
                    if self.levels[i].rect.collidepoint(event.pos[0],event.pos[1]):
                        game_start(i+1, self.continent, self.difficult)
                if self.button_return.rect.collidepoint(event.pos[0],event.pos[1]):
                    difficult_start(self.continent)

    def draw(self,screen):
        screen.blit(self.background,(0,0))
        self.buttons_levels.draw(screen)
        self.califications_levels.draw(screen)
        for i in range(0,15):
            self.text_numbers[i].draw(screen)
        self.title.draw(screen)
        pygame.display.flip()      
        
class WorldSelector():
    def __init__(self):
        self.background = pygame.image.load('resources/background_continent.png').convert()
        self.button_return= Button('resources/button_return.png',100,650)

        #Buttons creation
        self.button_Africa = Button('resources/button_Africa.png',110,400)
        self.button_America = Button('resources/button_America.png',310,400)
        self.button_Asia = Button('resources/button_Asia.png',510,400)
        self.button_Europe = Button('resources/button_Europe.png',710,400)
        self.button_Australia = Button('resources/button_Australia.png',910,400)

        self.buttons_continent = pygame.sprite.Group()
        self.buttons_continent.add(self.button_Africa)
        self.buttons_continent.add(self.button_America)
        self.buttons_continent.add(self.button_Asia)
        self.buttons_continent.add(self.button_Europe)
        self.buttons_continent.add(self.button_Australia)
        self.buttons_continent.add(self.button_return)

        #Configuration Files
        self.configuration = CfgUtils('configuration/configuration.cfg')
        self.languageID = self.configuration.read('Options','language')
        self.language = CfgUtils('configuration/language.cfg')
        self.rating_continent = CfgUtils('configuration/levels_rating.cfg')

        #Fonts
        self.fonts = {
                    'large' : pygame.font.Font('resources/CrashLandingBB.ttf',100), 
                    'small' : pygame.font.Font('resources/ThrowMyHandsUpintheAirBold.ttf',50),
                    'small2' : pygame.font.Font('resources/ThrowMyHandsUpintheAirBold.ttf',25)
        }  

        #Colors
        self.white = (255,255,255)

        #Ratings
        self.rating_Africa = int(self.rating_continent.read("AfricaTotal","rating"))
        self.rating_America = int(self.rating_continent.read("AmericaTotal","rating"))
        self.rating_Asia = int(self.rating_continent.read("AsiaTotal","rating"))
        self.rating_Australia = int(self.rating_continent.read("AustraliaTotal","rating"))
        self.rating_Europe = int(self.rating_continent.read("EuropeTotal","rating"))

        #Text
        self.title = Text(self.fonts['large'],self.language.read(self.languageID,'continent'),self.white,SCREEN_WIDTH/2,70)

        self.text_Africa = Text(self.fonts['small'],self.language.read(self.languageID,"africa"),self.white,110,300)
        self.text_America = Text(self.fonts['small'],self.language.read(self.languageID,"america"),self.white,310,300)
        self.text_Asia = Text(self.fonts['small'],self.language.read(self.languageID,"asia"),self.white,510,300)
        self.text_Australia = Text(self.fonts['small'],self.language.read(self.languageID,"europe"),self.white,710,300)
        self.text_Europe = Text(self.fonts['small'],self.language.read(self.languageID,"Australia"),self.white,910,300)

        self.text_rating_Africa = Text(self.fonts['small2'],str(self.rating_Africa)+"/135",self.white,110,510)
        self.text_rating_America = Text(self.fonts['small2'],str(self.rating_America)+"/135",self.white,310,510)
        self.text_rating_Asia = Text(self.fonts['small2'],str(self.rating_Asia)+"/135",self.white,510,510)
        self.text_rating_Australia = Text(self.fonts['small2'],str(self.rating_Australia)+"/135",self.white,710,510)
        self.text_rating_Europe = Text(self.fonts['small2'],str(self.rating_Europe)+"/135",self.white,910,510)

        #Rotation text's surfaces
        self.text_Africa.rotate(50)
        self.text_America.rotate(50)
        self.text_Asia.rotate(50)
        self.text_Australia.rotate(50)
        self.text_Europe.rotate(50)
    
    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

            if event.type == MOUSEBUTTONDOWN:
                if self.button_Africa.rect.collidepoint(event.pos[0],event.pos[1]):
                    difficult_start("Africa")
                if self.button_America.rect.collidepoint(event.pos[0],event.pos[1]):
                    difficult_start("America")
                if self.button_Asia.rect.collidepoint(event.pos[0],event.pos[1]):
                    difficult_start("Asia")
                if self.button_Australia.rect.collidepoint(event.pos[0],event.pos[1]):
                    difficult_start("Australia")
                if self.button_Europe.rect.collidepoint(event.pos[0],event.pos[1]):
                    difficult_start("Europe")
                if self.button_return.rect.collidepoint(event.pos[0],event.pos[1]):
                    global scene
                    scene = Menu()

    def draw(self,screen):
        screen.blit(self.background,(0,0))
        self.title.draw(screen)
        self.buttons_continent.draw(screen)
        self.text_Africa.draw(screen)
        self.text_America.draw(screen)
        self.text_Asia.draw(screen)
        self.text_Australia.draw(screen)
        self.text_Europe.draw(screen)
        self.text_rating_Africa.draw(screen)
        self.text_rating_America.draw(screen)
        self.text_rating_Asia.draw(screen)
        self.text_rating_Australia.draw(screen)
        self.text_rating_Europe.draw(screen)
        pygame.display.flip()

class Credits():
    def __init__(self):
        self.background = pygame.image.load('resources/background_credits.png')
        self.button_return= Button('resources/button_return.png',100,650)

        #Read configuration
        self.configuration = CfgUtils('configuration/configuration.cfg')
        self.language = CfgUtils('configuration/language.cfg')
        self.languageID = self.configuration.read('Options','language')

        self.mainidea = self.language.read(self.languageID,"mainidea")
        self.developer = self.language.read(self.languageID,"developer")
        self.designer = self.language.read(self.languageID,"designer")
        self.thanks = self.language.read(self.languageID,"thanks")

        #Fonts
        self.fonts = {
                    'large' : pygame.font.Font('resources/CrashLandingBB.ttf',170), 
                    'medium' : pygame.font.Font('resources/ThrowMyHandsUpintheAirBold.ttf',40),
        } 

        #Colors
        self.white = (255,255,255)

        #Text
        self.text_mainidea = Text(self.fonts['medium'],self.mainidea,self.white,SCREEN_WIDTH/2,650)
        self.text_developer = Text(self.fonts['medium'],self.developer,self.white,SCREEN_WIDTH/2,800)
        self.text_designer = Text(self.fonts['medium'],self.designer,self.white,SCREEN_WIDTH/2,950)
        self.text_thanks = Text(self.fonts['medium'],self.thanks,self.white,SCREEN_WIDTH/2,1100)

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if self.button_return.rect.collidepoint(event.pos[0],event.pos[1]):
                    global scene
                    scene = Menu()

        self.text_mainidea.rect.y -= 5
        self.text_developer.rect.y -= 5
        self.text_designer.rect.y -= 5
        self.text_thanks.rect.y -= 5
        if self.text_thanks.rect.y<=20:
            scene = Menu()
    
    def draw(self,screen):
        screen.blit(self.background,(0,0))      
        screen.blit(self.button_return.image,self.button_return.rect)
        self.text_mainidea.draw(screen)
        self.text_developer.draw(screen)
        self.text_designer.draw(screen)
        self.text_thanks.draw(screen)
        pygame.display.flip()
        
class Game():
    def __init__(self, level, continent, difficult):
        self.level = level
        self.continent = continent
        self.difficult = difficult

        #Read configurarion
        self.configuration = CfgUtils('configuration/configuration.cfg')
        self.languageID = self.configuration.read('Options','language')
        self.language = CfgUtils('configuration/language.cfg')

        self.rating_level = CfgUtils('configuration/levels_rating.cfg')
        self.current_rating_level = int(self.rating_level.read(self.continent+self.difficult,str(self.level)))

        self.levels_namescfg = CfgUtils('configuration/levels_names.cfg')

        self.path = "resources/levels/"+self.continent+"/"

        #Colors
        self.black = (0,0,0)
        self.white = (255,255,255)

        #Level Creator
        for Level in range(1,16):
            if Level==self.level:
                self.background = pygame.image.load(self.path+'bglevel'+str(Level)+'.jpg').convert()
                self.name = self.levels_namescfg.read(self.continent,"bglevel"+str(self.level))
        
        self.font = pygame.font.Font('resources/ThrowMyHandsUpintheAirBold.ttf',35)        
        self.level_title = Text(self.font,self.name,self.black,SCREEN_WIDTH/2,30)
        
        self.text_nextlevel = Text(self.font,self.language.read(self.languageID,'nextlevel'),self.white,1124,650)
        self.text_nextlevel.rotate(5)

        #Timer 
        self.timer = Timer()
        self.timer.start()

        self.star = Star(self.difficult)        
        self.button_nextlevel = ButtonNextLevel()
        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.star)
        self.sprites.add(self.button_nextlevel)

        self.title_shadow = pygame.image.load('resources/sombra_titulo_'+self.difficult+'.png').convert_alpha()

        #Pause instance
        self.pause = Pause()

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.pause.status=True                    
            if event.type == MOUSEBUTTONDOWN:
                if self.star.rect.collidepoint(event.pos[0],event.pos[1]):
                    self.button_nextlevel.move = True
                    if android:
                        android.vibrate(1)
                    self.star.move = True
                    if self.timer.time()<2:
                        #Write rating of level and total rating of continent
                        self.rating_level.write(self.continent+self.difficult,str(self.level),3)
                        self.rating_level.write(self.continent+"Total","rating",int(self.rating_level.read(self.continent+"Total","rating"))+3)
                    elif self.timer.time()>=2 and self.timer.time()<= 4:
                        if self.current_rating_level == 3:
                            pass
                        else:
                            #Write rating of level and total rating of continent
                            self.rating_level.write(self.continent+self.difficult,str(self.level),2)
                            self.rating_level.write(self.continent+"Total","rating",int(self.rating_level.read(self.continent+"Total","rating"))+2)
                    elif self.timer.time()> 4:
                        if self.current_rating_level == 2 or self.current_rating_level == 3:
                            pass
                        else:
                            #Write rating of level and total rating of continent
                            self.rating_level.write(self.continent+self.difficult,str(self.level),1)
                            self.rating_level.write(self.continent+"Total","rating",int(self.rating_level.read(self.continent+"Total","rating"))+1)
                    self.timer.stop()
                if self.button_nextlevel.rect.collidepoint(event.pos[0],event.pos[1]):
                    if self.level==15:
                        levelsselector_start(self.continent,self.difficult)
                    else:
                        game_start(self.level+1, self.continent, self.difficult)

        self.star.update()  

        if self.button_nextlevel.move:
            self.text_nextlevel.rect.x -= 10
            if self.text_nextlevel.rect.x<=740:
                self.text_nextlevel.rect.x = 740
            self.button_nextlevel.update()
            
    def draw(self,screen):
        #self.texto_temporizador para que no de error el draw.
        #self.texto_temporizador = Texto(self.fuente, self.temporizador.time(),self.color,SCREEN_WIDTH/2,60)

        screen.blit(self.background,(0,0))
        screen.blit(self.title_shadow,(0,0))
        self.level_title.draw(screen)
        #self.texto_temporizador.draw(screen)
        self.sprites.draw(screen)
        self.text_nextlevel.draw(screen)
        
        pygame.display.flip()
        #Instance pause with funcion update. Parameters: screen. __draw()
        self.pause.update(screen)

class Pause():
    def __init__(self):
        self.background = pygame.image.load('resources/background_pause.png').convert_alpha()
        self.rect_buttons = pygame.image.load('resources/rect_buttons.png').convert()
        self.button_play = Button('resources/button_playgame.png',250,350)
        self.button_reboot = Button('resources/button_playreboot.png',100,200)
        self.button_tolevels = Button('resources/button_playtolevels.png',100,500)

        self.buttons = pygame.sprite.Group()
        self.buttons.add(self.button_play)
        self.buttons.add(self.button_reboot)
        self.buttons.add(self.button_tolevels)

        self.status = False
        self.move = True
        self.gamereboot = False
        self.tolevels = False

        self.rect_buttons_x = -300

    def update(self,screen):
        while self.status:
            for event in pygame.event.get():     
                if event.type == MOUSEBUTTONDOWN:
                    if self.button_play.rect.collidepoint(event.pos[0],event.pos[1]):
                        self.move = False
                    if self.button_reboot.rect.collidepoint(event.pos[0],event.pos[1]):
                        self.gamereboot = True
                        self.move = False
                    if self.button_tolevels.rect.collidepoint(event.pos[0],event.pos[1]):
                        self.tolevels = True
                        self.move = False                        

            if self.move:
                self.rect_buttons_x += 15
                if self.rect_buttons_x>=0:
                    self.rect_buttons_x=0
            if self.move==False:
                self.rect_buttons_x -= 15
                if self.rect_buttons_x<=-300:
                    self.status = False
                    self.move = True
                    if self.gamereboot:
                        game_start(scene.level,scene.continent,scene.difficult)
                    if self.tolevels:
                        levelsselector_start(scene.continent,scene.difficult)

            #Bug fix button tolevels (scene levelselector)
            if self.status:
                self.__draw(screen)           

    def __draw(self,screen):
        #Not loss images of previous scene
        screen.blit(scene.background,(0,0))
        screen.blit(scene.title_shadow,(0,0))
        scene.level_title.draw(screen)
        scene.sprites.draw(screen)
        scene.text_nextlevel.draw(screen)

        screen.blit(self.background,(0,0))
        screen.blit(self.rect_buttons,(self.rect_buttons_x,0))
        if self.rect_buttons_x==0:
            self.buttons.draw(screen)
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

def credits_start():
    print "Changed scene to Credits()"
    global scene
    scene = Credits()

def worldselector_start():
    print "Changed scene to WorldSelector()"
    global scene
    scene = WorldSelector()

def difficult_start(continent):
    print "Changed scene to Difficult()"
    global scene
    scene = Difficult(continent)    

def levelsselector_start(continent,difficult):
    print "Changed scene to LevelsSelector " + difficult 
    global scene
    scene = LevelsSelector(continent,difficult)


'''####################################################
#              MAIN LOOP                           #
####################################################
''' 
def main():
    global scene
    pygame.init()
    
    clock = pygame.time.Clock()

    scene = Menu()

    if android:
        android.init() #Android start
        android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE) #mapkey for Android    
        #android_mixer.music.load('resources/background_music.mp3')
        #android_mixer.music.play(-1)

    """if not android:
        pygame.mixer.music.load('resources/background_music.mp3')
        pygame.mixer.music.play(-1)
    """

    while True:
        clock.tick(60)
        #print clock.get_fps()   
        if android:
            if android.check_pause():
                android.wait_for_resume()
        scene.update()
        scene.draw(screen)

if __name__ == '__main__':
    main()
