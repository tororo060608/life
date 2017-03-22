#!/usr/bin/env python

import pygame
from pygame.locals import *
import math

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

            
    def draw(self,screen,offset):
        screen.blit(self.image,(self.x - offset[0],
                                self.y - offset[1]))

    def update(self,screen,offset):
        self.draw(screen,offset)

        
class Chara(Obj):
    def __init__(self,imagedict,x,y,hp,atk,defe,speed):
        Obj.__init__(self,x,y)
        self.action = "stand"
        self.dire = "front"
        self.imagedict = imagedict
        self.imgobj = self.imagedict[self.action][self.dire]
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
        self.invincibletime = 0

    def draw(self,screen,offset):
        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()
        draw_x = self.x + self.width / 2 - self.image_width / 2
        draw_y = self.y + self.height / 2 - self.image_height / 2
        screen.blit(self.image,(draw_x - offset[0],
                                draw_y - offset[1]))

    def animation(self,screen,offset):
        self.imgobj = self.imagedict[self.action][self.dire]
        self.animelist = self.imgobj.imagelist
        self.image = self.animelist[self.frame // self.animecycle
                                    % self.imgobj.num]
        self.draw(screen,offset)

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

    def damage(self,blt):
        dmg = blt.atk - self.defe
        if dmg < 0:
            dmg = 0
        return dmg

    def death(self):
        if self.hp <= 0:
            self.kill()
        
    def move(self,objgroup):
        self.obj_collide(objgroup)
        
    def update(self,screen,offset):
        self.death()
        self.animation(screen,offset)
        self.frame += 1

        
class Bullet(Obj):
    def __init__(self,x,y,width,height,atk,speed,
                 time,filename = None):
        Obj.__init__(self,x,y,filename)
        self.width = width
        self.height = height
        self.rect = Rect(self.x,self.y,self.width,self.height)
        self.atk = atk
        self.speed = speed
        self.time = time
        self.frame = 0

    def move(self):
        self.x += self.speed
        self.y += self.speed
        self.rect = Rect(self.x,self.y,self.width,self.height)

    def vanish(self):
        if self.frame > self.time:
            self.kill()

    def update(self,screen):
        self.frame += 1
        self.move()
        self.vanish()
        
