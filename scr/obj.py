#!/usr/bin/env python

import pygame
from pygame.locals import *

import image

class Obj(pygame.sprite.Sprite):
    def __init__(self,x,y,filename=None):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.filename = filename
        self.x = x
        self.y = y
        
        if self.filename != None:
            self.image = image.load_image(self.filename)
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.rect = Rect(x,y,self.width,self.height)

            
    def draw(self,screen):
        screen.blit(self.image,(self.x,self.y))

    def update(self,screen):
        self.draw(screen)

class Chara(Obj):
    def __init__(self,imagedict,x,y,hp,atk,defe,speed):
        Obj.__init__(self,x,y)
        self.action = "fstand"
        self.imagedict = imagedict
        self.imgobj = self.imagedict[self.action]
        self.animelist = self.imgobj.imagelist
        self.image = self.animelist[0]
        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = Rect(self.x,self.y,self.width,self.height)
        self.frame = 0
        self.animecycle = 12
        self.hp = hp
        self.atk = atk
        self.defe = defe
        self.speed = speed
        self.vx = 0
        self.vy = 0
        
    def draw(self,screen):
        draw_x = self.x + self.width / 2 - self.image_width
        draw_y = self.y + self.height / 2 - self.image_height
        screen.blit(self.image,(draw_x,draw_y))

    def animetion(self,screen):
        self.imgobj = self.imagedict[self.action]
        self.animelist = self.imgobj.imagelist
        self.image = self.animelist[self.frame // self.animecycle
                                    % self.imgobj.num]
        self.draw(screen)
        
    def update(self,screen):
        self.animetion(screen)

        
class MyChara(Chara):
    def __init__(self,imagedict,x,y,hp,atk,defe,speed,stamina):
        Chara.__init__(self,imagedict,x,y,hp,atk,defe,speed)
        self.stamina = stamina

    def switch_moment(self,pre_action):
        if self.action != pre_action:
            self.frame = 0

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.vx = 0
        self.vy = 0

    def attack(self):
        pass

    def update(self,screen):
        Chara.update(self,screen)
        self.move()

class Enemy(Chara):
    def __init__(self,imagedict,x,y,hp,atk,defe,speed):
        Chara.__init__(self,imagedict,x,y,hp,atk,defe,speed)


def make_obj(GS,maplist,dict):
    e = dict["enemy"]
        
    for y,row in enumerate(maplist):
        for x,obj in enumerate(row):
            if obj == "w":
                Obj(GS*x,GS*y,"../picture/obj/wall.png")
            if obj == "e":
                status = e["statusdict"]
                Enemy(e["imagedict"],GS * x,GS * y,status["hp"],
                      status["atk"],status["defe"],status["speed"])
                
