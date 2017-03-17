#!/usr/bin/env python

import pygame
from pygame.locals import *

import obj
import enemy

def load_map(filename):
    map = []
    fp = open(filename,"r")
    for line in fp:
        line = line.rstrip()
        map.append(list(line))
    fp.close()
    return map


def make_map(GS,maplist,dict):
    ene = dict["enemy"]
    b = ene["boar"]
        
    for y,row in enumerate(maplist):
        for x,object in enumerate(row):
            if object == "w":
                obj.Obj(GS*x,GS*y,"../picture/obj/wall.png")
            if object == "b":
                status = b["statusdict"]
                enemy.Boar(b["imagedict"],GS * x,GS * y,status["hp"],
                      status["atk"],status["defe"],status["speed"])
