#!/usr/bin/env python

import pygame
from pygame.locals import *
import sys


SCREEN_SIZE = (640,480)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)

import stage

class Game():
    def __init__(self,stagelist,screen,mcdict):
        self.sceen = "title"
        self.screen = screen
        self.stagelist = stagelist
        self.stage = self.stagelist[0]
        self.mcdict = mcdict
        ms = mcdict["statusdict"]
        self.mchara = stage.mc.MyChara(mcdict["imagedict"],50,50,
                              ms["hp"],ms["atk"],ms["defe"],
                              ms["speed"],ms["stamina"])
        
    def move(self,objgroup,targetgroup):
        self.mchara.move(objgroup)
        for e in self.stage.enemys:
            e.move(objgroup,targetgroup)
        for b in self.stage.Mybullets:
            b.move()
        
    def title(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
                if event.key == K_a:
                    self.sceen = "play"

    def play(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
                if event.key == K_a:
                    self.mchara.attack()
        self.stage.objs.update(self.screen)
        self.mchara.update(self.screen,self.stage.enemys)
        self.stage.enemys.update(self.screen,self.stage.mc,
                                 self.stage.Mybullets)
        self.stage.Mybullets.update(self.screen)
        self.move(self.stage.objs,self.stage.mc)

        if self.mchara.hp <= 0:
            self.sceen = "deadend"

    def deadend(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
                if event.key == K_a:
                    self.__init__(self.stagelist,self.screen,
                                  self.mcdict)
        
    def update(self):
        if self.sceen == "title":
            self.title()
        if self.sceen == "play":
            self.stage.draw(self.screen)
            self.play()
        if self.sceen == "deadend":
            self.deadend()


game = Game(stage.stagelist,SCREEN,stage.info.mcdict)
