#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

from Star import Star, StarsCalification, StarMove, ObjectMoveGoal
from Button import Button
from Text import Text
from Timer import Timer
from configuration import Configuration

import pytweener

import os
import platform
import math

os.environ['SDL_VIDEO_CENTERED'] = '1'
if platform.system() == 'Windows':
    os.environ['SDL_VIDEODRIVER'] = 'windib'

try:
    import android
except ImportError:
    android = None

print "Modules imported"

scene = None

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Where is the star?")
pygame.display.set_icon(pygame.image.load("resources/star.png").convert_alpha())

#Read configuration
Configuration = Configuration()
configuration = Configuration.configuration_json()

language_ = Configuration.language_json()
languageID = configuration['options']['language']

language = language_[languageID]

levels_rating = Configuration.levels_rating_json()


'''
####################8###############################
#                  SCENES                          #
####################################################zz
'''
class Menu():
    def __init__(self):
        self.background = pygame.image.load('resources/background_menu.png').convert()
        self.shadow_goal = pygame.image.load('resources/shadow_goal.png').convert_alpha()
        self.earth_planet = pygame.image.load('resources/earthplanet.png').convert_alpha()

        #Buttons creation
        self.button_play = Button('resources/button_play.png',SCREEN_WIDTH/2,400)
        self.button_logo = Button('resources/logo.png',SCREEN_WIDTH/2,140)

        self.buttons = pygame.sprite.Group()
        self.buttons.add(self.button_play)
        self.buttons.add(self.button_logo)

        #Stars
        self.stars = pygame.sprite.Group()
        for i in range(10):
            self.stars.add(StarMove())

        #Fonts
        self.fonts = {
                    'large' : pygame.font.Font("resources/CrashLandingBB.ttf",120),
                    'middle' : pygame.font.Font("resources/CrashLandingBB.ttf",40),
                    'small' : pygame.font.Font("resources/ThrowMyHandsUpintheAirBold.ttf",30)
        }

        #Colors
        self.white = (255,255,255)

        self.text_play = Text(self.fonts['large'],language['play'],self.white,SCREEN_WIDTH/2,400)
        self.text_goal = Text(self.fonts['small'],language['goal'],self.white,1900,650)

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                exit()

            if event.type == MOUSEBUTTONDOWN:
                if self.button_play.rect.collidepoint(event.pos[0],event.pos[1]):
                    worldselector_start()
                if self.button_logo.rect.collidepoint(event.pos[0],event.pos[1]):
                        self.credits = Credits()
                        self.credits.status = True
                        self.credits.update(screen)
        self.stars.update()

        self.text_goal.rect.x -= 2.5
        if self.text_goal.rect.x < -1350:
            self.text_goal.rect.x = 1900

    def draw(self,screen):
        screen.blit(self.background,(0,0))
        self.stars.draw(screen)
        screen.blit(self.earth_planet,(176,500))
        self.buttons.draw(screen)
        self.text_play.draw(screen)
        screen.blit(self.shadow_goal,(0,625))
        self.text_goal.draw(screen)
        pygame.display.flip();

class Difficult():
    def __init__(self,continent):
        self.continent = continent

        self.background = pygame.image.load('resources/background_difficult.png').convert()

        #Buttons creation
        self.button_easy = Button('resources/Boton_dificultad1.png',512,250)
        self.button_medium = Button('resources/Boton_dificultad2.png',512,375)
        self.button_hard = Button('resources/Boton_dificultad3.png',512,500)

        self.buttons = pygame.sprite.Group()
        self.buttons.add(self.button_easy)
        self.buttons.add(self.button_medium)
        self.buttons.add(self.button_hard)

        #Fonts
        self.fonts = {
                    'large' : pygame.font.Font('resources/CrashLandingBB.ttf',170),
                    'medium' : pygame.font.Font('resources/ThrowMyHandsUpintheAirBold.ttf',85),
        }

        #Colors
        self.white = (255,255,255)

        self.title = Text(self.fonts['large'],language['dificult'],self.white,512,70)
        self.text_easy = Text(self.fonts['medium'],language['easy'],self.white,512,250)
        self.text_medium = Text(self.fonts['medium'],language['medium'],self.white,512,375)
        self.text_hard = Text(self.fonts['medium'],language['hard'],self.white,512,500)

        print "Difficult() created"

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                worldselector_start()
            if event.type == MOUSEBUTTONDOWN:
                if self.button_easy.rect.collidepoint(event.pos[0],event.pos[1]):
                    levelsselector_start(self.continent,"Easy")
                if self.button_medium.rect.collidepoint(event.pos[0],event.pos[1]):
                    levelsselector_start(self.continent,"Medium")
                if self.button_hard.rect.collidepoint(event.pos[0],event.pos[1]):
                    levelsselector_start(self.continent,"Hard")

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
        self.continent = continent
        self.difficult = difficult

        self.background = pygame.image.load('resources/background_'+self.difficult+'.jpg').convert()

        self.levels = []
        self.numbers = []
        self.text_numbers = []
        self.starscalification = []
        

        #Fonts
        self.fonts = {
                    'large' : pygame.font.Font('resources/CrashLandingBB.ttf',170),
                    'medium' : pygame.font.Font('resources/ThrowMyHandsUpintheAirBold.ttf',85),
        }

        #Colors
        self.white = (255,255,255)

        self.buttons_levels = pygame.sprite.Group()
        self.califications_levels = pygame.sprite.Group()
        self.numbers_levels = pygame.sprite.Group()

        self.title = Text(self.fonts['large'],language['levels'],self.white,512,70)


        self.califications = []
        for i in xrange(0,15):
            self.califications.append(int(levels_rating[self.continent+self.difficult][str(i+1)]))

        for i in xrange(0, 15):
            if self.califications[i-1] == 3 or i == 0:
                self.status = ''
            else:
                self.status = '_lock'
            if i < 5:
                if self.status == '':
                    self.text_numbers.append(Text(self.fonts['medium'],str(i+1),self.white,174+175*i,250))
                    self.starscalification.append(StarsCalification(self.califications[i],174+175*i,295))
                    self.numbers_levels.add(self.text_numbers[-1])
                    self.califications_levels.add(self.starscalification[-1])
                self.levels.append(Button('resources/button_'+self.difficult+self.status+'.png',174+175*i,250))

            elif i>=5 and i<10:
                if self.status == '':
                    self.text_numbers.append(Text(self.fonts['medium'],str(i+1),self.white,174+175*i-875,425))
                    self.starscalification.append(StarsCalification(self.califications[i],174+175*i-875,470))
                    self.numbers_levels.add(self.text_numbers[-1])
                    self.califications_levels.add(self.starscalification[-1])
                self.levels.append(Button('resources/button_'+self.difficult+self.status+'.png',174+175*i-875,425))

            elif i>=10:
                if self.status == '':
                    self.text_numbers.append(Text(self.fonts['medium'],str(i+1),self.white,174+175*i-1750,600))
                    self.starscalification.append(StarsCalification(self.califications[i],174+175*i-1750,645))
                    self.numbers_levels.add(self.text_numbers[-1])
                    self.califications_levels.add(self.starscalification[-1])
                self.levels.append(Button('resources/button_'+self.difficult+self.status+'.png',174+175*i-1750,600))

            self.buttons_levels.add(self.levels[i])

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                difficult_start(self.continent)
            if event.type == MOUSEBUTTONDOWN:
                for i in range(0,15):
                    if self.levels[i].rect.collidepoint(event.pos[0],event.pos[1]):
                        if self.califications[i-1] == 3 or i == 0:
                            game_start(i+1, self.continent, self.difficult)

    def draw(self,screen):
        screen.blit(self.background,(0,0))
        self.buttons_levels.draw(screen)
        self.califications_levels.draw(screen)
        self.numbers_levels.draw(screen)
        self.title.draw(screen)
        pygame.display.flip()

class WorldSelector():
    def __init__(self):
        self.background = pygame.image.load('resources/background_continent.png').convert()

        #Ratings
        self.rating_Africa = 0
        self.rating_America = 0
        self.rating_Asia = 0
        self.rating_Australia = 0
        self.rating_Europe = 0

        for i in range(1,16):
            self.rating_Africa += int(levels_rating['AfricaEasy'][str(i)])
            self.rating_Africa += int(levels_rating["AfricaMedium"][str(i)])
            self.rating_Africa += int(levels_rating["AfricaHard"][str(i)])

            self.rating_America += int(levels_rating["AmericaEasy"][str(i)])
            self.rating_America += int(levels_rating["AmericaMedium"][str(i)])
            self.rating_America += int(levels_rating["AmericaHard"][str(i)])

        #Fonts
        self.fonts = {
                    'large' : pygame.font.Font('resources/CrashLandingBB.ttf',100),
                    'small' : pygame.font.Font('resources/ThrowMyHandsUpintheAirBold.ttf',50),
                    'small2' : pygame.font.Font('resources/ThrowMyHandsUpintheAirBold.ttf',25)
        }

        #Colors
        self.white = (255,255,255)

        self.text = pygame.sprite.Group()

        self.title = Text(self.fonts['large'],language['continent'],self.white,SCREEN_WIDTH/2,70)

        self.text_Africa = Text(self.fonts['small'],language["africa"],self.white,110,300)
        self.text_rating_Africa = Text(self.fonts['small2'],str(self.rating_Africa)+"/135",self.white,110,510)
        self.text_Africa.rotate(50)

        #Levels Unlocked
        if self.rating_Africa == 135:
            self.button_America_image = 'resources/button_America.png'

            self.text_America = Text(self.fonts['small'],language["america"],self.white,310,300)
            self.text_rating_America = Text(self.fonts['small2'],str(self.rating_America)+"/135",self.white,310,510)
            self.text_America.rotate(50)

            self.text.add(self.text_America)
            self.text.add(self.text_rating_America)
        else:
            self.button_America_image = 'resources/button_America_lock.png'

        #Buttons creation
        self.button_Africa = Button('resources/button_Africa.png', 110, 400)
        self.button_America = Button(self.button_America_image,310,400)
        self.button_Asia = Button('resources/button_Asia_lock.png',510,400)
        self.button_Europe = Button('resources/button_Europe_lock.png',710,400)
        self.button_Australia = Button('resources/button_Australia_lock.png',910,400)

        self.buttons_continent = pygame.sprite.Group()
        self.buttons_continent.add(self.button_Africa)
        self.buttons_continent.add(self.button_America)
        self.buttons_continent.add(self.button_Asia)
        self.buttons_continent.add(self.button_Europe)
        self.buttons_continent.add(self.button_Australia)

        self.text.add(self.title)
        self.text.add(self.text_Africa)
        self.text.add(self.text_rating_Africa)

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                global scene
                scene = Menu()

            if event.type == MOUSEBUTTONDOWN:
                if self.button_Africa.rect.collidepoint(event.pos[0],event.pos[1]):
                    difficult_start("Africa")

                if self.button_America.rect.collidepoint(event.pos[0],event.pos[1]):
                    if self.rating_Africa == 135:
                        difficult_start("America")

    def draw(self,screen):
        screen.blit(self.background,(0,0))
        self.buttons_continent.draw(screen)
        self.text.draw(screen)
        pygame.display.flip()

class Credits():
    def __init__(self):
        self.background = pygame.image.load('resources/background_credits.png').convert_alpha()
        self.logo = pygame.image.load('resources/logomini.png').convert_alpha()

        #Fonts
        self.fonts = {
                    'large' : pygame.font.Font('resources/CrashLandingBB.ttf',130),
                    'medium' : pygame.font.Font('resources/ThrowMyHandsUpintheAirBold.ttf',40),
        }

        #Colors
        self.white = (255,255,255)

        #Text
        self.text_credits  = Text(self.fonts['large'],language['credits'],self.white,SCREEN_WIDTH/2,70)
        self.text_mainidea = Text(self.fonts['medium'],language['mainidea'],self.white,SCREEN_WIDTH/2,350)
        self.text_developer = Text(self.fonts['medium'],language['developer'],self.white,SCREEN_WIDTH/2,450)
        self.text_designer = Text(self.fonts['medium'],language['designer'],self.white,SCREEN_WIDTH/2,550)

        self.status = False
    def update(self,screen):
        while self.status:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    self.status = False

            scene.stars.update()

            self._draw(screen)

    def _draw(self,screen):
        screen.blit(scene.background,(0,0))
        scene.stars.draw(screen)
        screen.blit(scene.earth_planet,(176,500))

        screen.blit(self.background,(0,0))
        screen.blit(self.logo,(362,170))
        self.text_credits.draw(screen)
        self.text_mainidea.draw(screen)
        self.text_developer.draw(screen)
        self.text_designer.draw(screen)
        pygame.display.flip()

class Game():
    def __init__(self, level, continent, difficult):
        self.level = level
        self.continent = continent
        self.difficult = difficult

        self.current_rating_level = int(levels_rating[self.continent+self.difficult][str(self.level)])
        #Colors
        self.black = (0,0,0)
        self.white = (255,255,255)
        
        self.background = pygame.image.load('resources/levels/'+self.continent+'/bglevel'+str(self.level)+'.jpg').convert()
        self.name = Configuration.level_name_json(languageID, self.continent, self.level)

        self.font = pygame.font.Font('resources/ThrowMyHandsUpintheAirBold.ttf',35)
        self.level_title = Text(self.font,self.name,self.black,SCREEN_WIDTH/3+40,30)

        #Timer
        self.timer = Timer()

        self.tweener = pytweener.Tweener()

        self.star = Star(self.difficult)
        self.button_returnmenu = Button('resources/button_returnmenu.png',830,30)
        self.button_playreboot = Button('resources/button_playreboot.png',900,30)
        self.button_pause = Button('resources/button_pause.png',970,30)

        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.button_returnmenu)
        self.sprites.add(self.button_playreboot)
        self.sprites.add(self.button_pause)

        self.title_shadow = pygame.image.load('resources/sombra_titulo_'+self.difficult+'.png').convert_alpha()

        #Pause instance
        self.pause = Pause()

        #Game_Counter instance
        self.game_counter = GameCounter()

        self.clock = pygame.time.Clock()

    def update(self):
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if self.button_returnmenu.rect.collidepoint(event.pos[0],event.pos[1]):
                    levelsselector_start(self.continent,self.difficult)
                if self.button_pause.rect.collidepoint(event.pos[0],event.pos[1]):
                    self.timer.stop()
                    self.pause.status = True
                if self.button_playreboot.rect.collidepoint(event.pos[0],event.pos[1]):
                    game_start(self.level,self.continent,self.difficult)
                if not self.star.move:
                    if self.star.rect.collidepoint(event.pos[0],event.pos[1]):
                        if android:
                            android.vibrate(1)
                        self.star.move = True
                        self.star.image = self.star.image_move
                        self.tweener.addTween(self.star,x=1024,tweenTime=1, tweenType=pytweener.Easing.Elastic.easeIn)
                        if self.timer.time()<=4:
                            #Write rating of level and total rating of continent
                            levels_rating[self.continent+self.difficult][str(self.level)] = "3"
                            Configuration.override_rating_json(levels_rating)
                            self.level_goal = LevelGoal(3)
                        elif self.timer.time()>4 and self.timer.time()<= 6:
                            if self.current_rating_level == 3:
                                pass
                            else:
                                levels_rating[self.continent+self.difficult][str(self.level)] = "2"
                                Configuration.override_rating_json(levels_rating)
                            self.level_goal = LevelGoal(2)
                        elif self.timer.time()> 6:
                            if self.current_rating_level == 2 or self.current_rating_level == 3:
                                pass
                            else:
                                levels_rating[self.continent+self.difficult][str(self.level)] = "1"
                                Configuration.override_rating_json(levels_rating)
                            self.level_goal = LevelGoal(1)
                        self.timer.stop()

        #print self.timer.time()
        self.timer.time()
        self.dt = self.clock.tick(60)
        self.tweener.update(self.dt/1000.0)

    def draw(self,screen):
        screen.blit(self.background,(0,0))
        screen.blit(self.title_shadow,(0,0))
        self.level_title.draw(screen)
        self.sprites.draw(screen)

        screen.blit(self.star.image,(self.star.x,self.star.y))

        pygame.display.flip()
        #Instance pause with funcion update. Parameters: screen. __draw()
        self.pause.update(screen)

        #Instance GameCounter with funcion update. Parameters: screen. __draw()
        self.game_counter.update(screen)

        #Instance LevelGoal with funcion update. Parameters: screen. __draw()
        if self.star.x > 1000:
            self.level_goal.state = True
            self.level_goal.update(screen)

class GameCounter():
    def __init__(self):
        self.background = pygame.image.load('resources/background_pause.png').convert_alpha()

        self.counter = 10000
        self.state = True
        self.timer = Timer()

        self.font = pygame.font.Font('resources/ThrowMyHandsUpintheAirBold.ttf',300)
        self.text_counter = Text(self.font,self.counter,(255,255,255),SCREEN_WIDTH/2,SCREEN_HEIGHT/2)

        self.timer.start()

    def update(self,screen):
        while self.state:
            self.counter -= self.timer.time() * 100

            if self.counter < 0:
                self.state = False
                self.timer.stop()
                scene.timer.start()

            #make text in update, why is a object that renew
            self.text_counter = Text(self.font,int(math.ceil(self.counter/4000)),(255,255,255),SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
            self._draw(screen)

    def _draw(self,screen):
        #Doesnt loss images of previous scene
        screen.blit(scene.background,(0,0))
        screen.blit(scene.title_shadow,(0,0))
        scene.level_title.draw(screen)

        screen.blit(self.background,(0,0))
        self.text_counter.draw(screen)
        pygame.display.flip()

class LevelGoal():
    def __init__(self,score):
        self.background = pygame.image.load('resources/goal_screen.png').convert_alpha()
        self.score = score

        self.buttons = pygame.sprite.Group()

        self.button_returnmenu = Button('resources/button_returnmenu.png',470,580)

        self.stars = []

        if self.score == 1:
            self.stars.append(ObjectMoveGoal('resources/star_goal.png',355,750))
            self.stars.append(ObjectMoveGoal('resources/star_goalno.png',483,750))
            self.stars.append(ObjectMoveGoal('resources/star_goalno.png',605,750))

            self.button_playgame = Button('resources/button_playreboot.png',550,580)
        elif self.score == 2:
            self.stars.append(ObjectMoveGoal('resources/star_goal.png',355,750))
            self.stars.append(ObjectMoveGoal('resources/star_goalno.png',483,750))
            self.stars.append(ObjectMoveGoal('resources/star_goal.png',605,750))

            self.button_playgame = Button('resources/button_playreboot.png',550,580)
        elif self.score == 3:
            self.stars.append(ObjectMoveGoal('resources/star_goal.png',355,750))
            self.stars.append(ObjectMoveGoal('resources/star_goal.png',483,750))
            self.stars.append(ObjectMoveGoal('resources/star_goal.png',605,750))

            self.button_playgame = Button('resources/button_playgame.png',550,580)

        self.buttons.add(self.button_returnmenu)
        self.buttons.add(self.button_playgame)

        self.state = False
        self.state_return_menu = True

        self.tweener = pytweener.Tweener()

        self.tweener.addTween(self.stars[0],y=350,tweenTime=2.0,tweenType=pytweener.Easing.Elastic.easeOut)
        self.tweener.addTween(self.stars[1],y=300,tweenTime=3.0,tweenType=pytweener.Easing.Elastic.easeOut)
        self.tweener.addTween(self.stars[2],y=350,tweenTime=4.0,tweenType=pytweener.Easing.Elastic.easeOut)

    def update(self,screen):
        while self.state:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if self.button_returnmenu.rect.collidepoint(event.pos[0],event.pos[1]):
                        self.state = False
                        self.state_return_menu = False
                        levelsselector_start(scene.continent,scene.difficult)
                    elif self.button_playgame.rect.collidepoint(event.pos[0],event.pos[1]):
                        self.state = False
                        self.state_return_menu = False
                        if self.score==3:
                            if scene.level == 15:
                                levelsselector_start(scene.continent,scene.difficult)
                            else:
                                game_start(scene.level+1,scene.continent,scene.difficult)
                        else:
                            game_start(scene.level,scene.continent,scene.difficult)

            #Bug fix button_returnmenu (scene levelselector)
            if self.state_return_menu:
                self._draw(screen)
                #Take clock.tick of main scene = Game()
                self.tweener.update(scene.dt/1000.0)

    def _draw(self,screen):
        #Doesnt loss images of previous scene
        screen.blit(scene.background,(0,0))
        screen.blit(scene.title_shadow,(0,0))
        scene.level_title.draw(screen)

        screen.blit(self.background,(201,80))
        screen.blit(self.stars[0].image,(self.stars[0].x,self.stars[0].y))
        screen.blit(self.stars[1].image,(self.stars[1].x,self.stars[1].y))
        screen.blit(self.stars[2].image,(self.stars[2].x,self.stars[2].y))
        self.buttons.draw(screen)
        pygame.display.flip()

class Pause():
    def __init__(self):
        self.background = pygame.image.load('resources/background_pause.png').convert_alpha()
        self.button_play = Button('resources/button_playgame.png',760,30)

        self.font = pygame.font.Font('resources/ThrowMyHandsUpintheAirBold.ttf',300)
        self.text_pause = Text(self.font,language['pause'],(255,255,255),SCREEN_WIDTH/2,SCREEN_HEIGHT/2)

        self.buttons = pygame.sprite.Group()
        self.buttons.add(self.button_play)

        self.status = False

    def update(self,screen):
        while self.status:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if self.button_play.rect.collidepoint(event.pos[0],event.pos[1]):
                        scene.timer.resume()
                        self.status = False

            self._draw(screen)

    def _draw(self,screen):
        #Doesnt loss images of previous scene
        screen.blit(scene.background,(0,0))
        screen.blit(scene.title_shadow,(0,0))
        scene.level_title.draw(screen)
        scene.sprites.draw(screen)

        screen.blit(self.background,(0,0))
        self.text_pause.draw(screen)
        self.buttons.draw(screen)
        pygame.display.flip()

'''
####################################################
#               FUNCTIONS                          #
#              SCENE CHANGES                       #
####################################################
'''
def game_start(level, continent, difficult):
    global scene;
    scene = Game(level, continent, difficult)

def worldselector_start():
    global scene
    scene = WorldSelector()

def difficult_start(continent):
    global scene
    scene = Difficult(continent)

def levelsselector_start(continent,difficult):
    global scene
    scene = LevelsSelector(continent,difficult)


'''
####################################################
#              MAIN LOOP                           #
####################################################
'''
def main():
    global scene
    pygame.init()

    clock = pygame.time.Clock()

    scene = LevelsSelector("Africa","Easy")
    #scene = WorldSelector()
    #scene = Menu()
    #scene = Game(12,"America","Easy")

    if android:
        android.init()  #AndroidWorldSelec init
        android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)

    while True:
        clock.tick(60)
        if android:
            if android.check_pause():
                android.wait_for_resume()
        scene.update()
        scene.draw(screen)

if __name__ == '__main__':
    main()
