#!/usr/bin/env python

import pygame
from pygame.locals import *

import obj
import map
import info
import image
import enemy
import mc

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
        self.mc = pygame.sprite.Group()
        self.enemys = pygame.sprite.Group()
        self.objs = pygame.sprite.Group()
        self.Mybullets = pygame.sprite.Group()
        obj.Obj.containers = self.objs
        mc.MyChara.containers = self.mc
        mc.MyBullet.containers = self.Mybullets
        enemy.Enemy.containers = self.enemys
        map.make_map(self.GS,self.maplist,self.objdict)
        self.bgimg = image.load_image("../picture/obj/floor.png")
        
    def draw(self,screen):
        for y in range(self.row):
            for x in range(self.col):
                screen.blit(self.bgimg,(x * self.GS,y * self.GS))


stage1 = Stage("../lib/map/map1.txt",info.objdict)
stagelist = [stage1]
