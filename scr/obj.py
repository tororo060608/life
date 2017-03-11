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
        draw_x = self.x + self.width / 2 - self.image_width / 2
        draw_y = self.y + self.height / 2 - self.image_height / 2
        screen.blit(self.image,(draw_x,draw_y))

    def animetion(self,screen):
        self.imgobj = self.imagedict[self.action]
        self.animelist = self.imgobj.imagelist
        self.image = self.animelist[self.frame // self.animecycle
                                    % self.imgobj.num]
        self.draw(screen)

    def obj_collide(self,objgroup):
        newx = self.x + self.vx
        newrect = Rect(newx,self.y,self.width,self.height)
        for obj in objgroup:
            collide = newrect.colliderect(obj.rect)
            if collide:
                if self.vx > 0:
                    self.x = obj.rect.left - self.width
                    self.vx = 0
                elif self.vx < 0:
                    self.x = obj.rect.right
                    self.vx = 0
                break
            else:
                self.x = newx
        self.vx = 0
        
        newy = self.y + self.vy
        newrect = Rect(self.x,newy,self.width,self.height)
        for obj in objgroup:
            collide = newrect.colliderect(obj.rect)
            if collide:
                if self.vy > 0:
                    self.y = obj.rect.top - self.height
                    self.vy = 0
                elif self.vy < 0:
                    self.y = obj.rect.bottom
                    self.vy = 0
                break
            else:
                self.y = newy
        self.vy = 0
        
        self.rect = Rect(self.x,self.y,self.width,self.height)
        
    def move(self,objgroup):
        self.obj_collide(objgroup)
        
    def update(self,screen,objgroup):
        self.animetion(screen)
        self.move(objgroup)
        self.frame += 1
        
class MyChara(Chara):
    def __init__(self,imagedict,x,y,hp,atk,defe,speed,stamina):
        Chara.__init__(self,imagedict,x,y,hp,atk,defe,speed)
        self.stamina = stamina
        self.weapon_wide = 64
        self.weapon_length = 32

    def attack(self):
        if self.action == "lwalk" or self.action == "lstand":
            MyBullet(self.x - self.weapon_length,
                   self.y - (self.weapon_wide - self.height) / 2,
                   self.weapon_length,
                   self.weapon_wide,
                   self.atk,0)
        if self.action == "rwalk" or self.action == "rstand":
            MyBullet(self.x + self.weapon_length,
                   self.y - (self.weapon_wide - self.height) / 2,
                   self.weapon_length,
                   self.weapon_wide,
                   self.atk,0)
        if self.action == "fwalk" or self.action == "fstand":
            MyBullet(self.x - (self.weapon_wide - self.width) / 2,
                   self.y + self.height,
                   self.weapon_wide,
                   self.weapon_length,
                   self.atk,0)
        if self.action == "bwalk" or self.action == "bstand":
            MyBullet(self.x - (self.weapon_wide - self.width) / 2,
                   self.y - self.height,
                   self.weapon_wide,
                   self.weapon_length,
                   self.atk,0)
    
    def update(self,screen,objgroup):
        Chara.update(self,screen,objgroup)

class Enemy(Chara):
    def __init__(self,imagedict,x,y,hp,atk,defe,speed):
        Chara.__init__(self,imagedict,x,y,hp,atk,defe,speed)

class Bullet(Obj):
    def __init__(self,x,y,width,height,atk,speed,filename = None):
        Obj.__init__(self,x,y,filename)
        self.width = width
        self.height = height
        self.rect = Rect(self.x,self.y,self.width,self.height)
        self.atk = atk
        self.speed = speed

    def move(self):
        self.x += self.speed
        self.y += self.speed
        self.rect = Rect(self.x,self.y,self.width,self.height)

    def update(self,screen):
        self.move()

        
class MyBullet(Bullet):
    def __init__(self,x,y,width,height,atk,speed,filename = None):
        Bullet.__init__(self,x,y,width,height,atk,speed,filename)



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
                
