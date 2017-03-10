#!/usr/bin/env python

import pygame
from pygame.locals import *

import obj
import map
import info
import image


class Stage():
    GS = 32
    def __init__(self,mapfile,objdict):
        self.frame = 0
        self.objdict = objdict
        self.maplist = map.load_map(mapfile)
        self.row = len(self.maplist)
        self.col = len(self.maplist[0])
        self.width = self.col * self.GS
        self.height = self.row * self.GS
        self.all = pygame.sprite.Group()
        self.mc = pygame.sprite.Group()
        self.enemys = pygame.sprite.Group()
        obj.Obj.containers = self.all
        obj.MyChara.containers = self.all,self.mc
        obj.Enemy.containers = self.all,self.enemys
        obj.make_obj(self.GS,self.maplist,self.objdict)
        self.bgimg = image.load_image("../picture/obj/floor.png")
        
        
    def draw(self,screen):
        for y in range(self.row):
            for x in range(self.col):
                screen.blit(self.bgimg,(x * self.GS,y * self.GS))


stage1 = Stage("../lib/map/map1.txt",info.objdict)
stagelist = [stage1]
