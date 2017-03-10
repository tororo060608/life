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
        ms = mcdict["statusdict"]
        self.mchara = stage.obj.MyChara(mcdict["imagedict"],50,50,
                              ms["hp"],ms["atk"],ms["defe"],
                              ms["speed"],ms["stamina"])
        
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
                if event.type == KEYDOWN:
                    if event.key == K_a:
                        print("a")
        pressed_key = pygame.key.get_pressed()
        if pressed_key[K_LEFT]:
            self.mchara.vx = -self.mchara.speed
        if pressed_key[K_RIGHT]:
            self.mchara.vx = self.mchara.speed
        if pressed_key[K_DOWN]:
            self.mchara.vy = self.mchara.speed
        if pressed_key[K_UP]:
            self.mchara.vy = -self.mchara.speed

        self.stage.all.update(self.screen)

                
    def update(self):
        if self.sceen == "title":
            self.title()
        if self.sceen == "play":
            self.stage.draw(self.screen)
            self.play()


game = Game(stage.stagelist,SCREEN,stage.info.mcdict)