#!/usr/bin/env python

import pygame
from pygame.locals import *

pygame.init()

def load_image(filename,colorkey = None):
    image = pygame.image.load(filename).convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey,RLEACCEL)
    return image


def split_image(image,num,colorkey = None):
    width = image.get_width()
    height = image.get_height()
    imagelist = []
    size = width / num
    for i in range(0,num):
        surface = pygame.Surface((width,height))
        surface.blit(image,(0,0),(i * size,0,width,height))
        surface.set_colorkey(surface.get_at((0,0)),RLEACCEL)
        surface.convert()
        imagelist.append(surface)
    return imagelist


class Images():
    def __init__(self,filename,num,colorkey=None):
        self.num = num
        self.image = load_image(filename,colorkey)
        self.imagelist = split_image(self.image,self.num)
        


