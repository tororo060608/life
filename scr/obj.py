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

            
    def draw(self,screen):
        screen.blit(self.image,(self.x,self.y))

    def update(self,screen):
        self.draw(screen)

        
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
        self.bullettime = 35

    def draw(self,screen):
        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()
        draw_x = self.x + self.width / 2 - self.image_width / 2
        draw_y = self.y + self.height / 2 - self.image_height / 2
        screen.blit(self.image,(draw_x,draw_y))

    def animation(self,screen):
        self.imgobj = self.imagedict[self.action][self.dire]
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
        self.animation(screen)
        self.move(objgroup)
        self.frame += 1
        
class MyChara(Chara):
    def __init__(self,imagedict,x,y,hp,atk,defe,speed,stamina):
        Chara.__init__(self,imagedict,x,y,hp,atk,defe,speed)
        self.stamina = stamina
        self.weapon_wide = 64
        self.weapon_length = 32

    def attack(self):
        if self.action == "hit": return
        if self.action not in ["attack","stop"]:
            self.frame = 0
            self.action = "attack"
            if self.dire == "left":
                MyBullet(self.x - self.weapon_length,
                         self.y-(self.weapon_wide - self.height) /2,
                         self.weapon_length,
                         self.weapon_wide,
                         self.atk,0,self.bullettime)
            if self.action == "right":
                MyBullet(self.x + self.weapon_length,
                         self.y-(self.weapon_wide - self.height) /2,
                         self.weapon_length,
                         self.weapon_wide,
                         self.atk,0,self.bullettime)
            if self.action == "front":
                MyBullet(self.x-(self.weapon_wide - self.width) / 2,
                         self.y + self.height,
                         self.weapon_wide,
                         self.weapon_length,
                         self.atk,0,self.bullettime)
            if self.action == "back":
                MyBullet(self.x-(self.weapon_wide - self.width) / 2,
                         self.y - self.height,
                         self.weapon_wide,
                         self.weapon_length,
                         self.atk,0,self.bullettime)
            
    def walk(self):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[K_LEFT]:
            self.vx = -self.speed
            self.dire = "left"
            self.action = "walk"
        if pressed_key[K_RIGHT]:
            self.vx = self.speed
            self.dire = "right"
            self.action = "walk"
        if pressed_key[K_DOWN]:
            self.vy = self.speed
            self.dire = "front"
            self.action = "walk"
        if pressed_key[K_UP]:
            self.vy = -self.speed
            self.dire = "back"
            self.action = "walk"
        if self.vx != 0 and self.vy != 0:
            self.vx = self.vx * 1.41 / 2
            self.vy = self.vy * 1.41 / 2
            
    def stand(self):
        pressed_key = pygame.key.get_pressed()
        if not 1 in pressed_key:
            self.action = "stand"

    def stop(self):
        if self.action == "stop" and self.frame > 10:
            self.action = "stand"
            self.frame = 0

    def hit_enemy(self,enemys):
        if self.invincibletime > 50:
            self.invincibletime = 0
        if self.action == "hit" or self.invincibletime:
            self.invincibletime += 1
            return
        for enemy in enemys:
            collide = self.rect.colliderect(enemy)
            if collide:
                self.action = "hit"
                self.frame = 0
                self.invincibletime += 1
                dx = enemy.rect.centerx - self.rect.centerx
                dy = enemy.rect.centery - self.rect.centery
                rad = math.atan2(dy,dx)
                self.vx = - self.speed * math.cos(rad) * 2
                self.vy = - self.speed * math.sin(rad) * 2
                if math.fabs(dx) > math.fabs(dy):
                    if dx > 0:
                        self.dire = "right"
                    elif dx < 0:
                        self.dire = "left"
                if math.fabs(dx) < math.fabs(dy):
                    if dy > 0:
                        self.dire = "front"
                    if dy < 0:
                        self.dire = "back"
                break
                
    def update(self,screen,objgroup,enemygroup):
        self.hit_enemy(enemygroup)
        self.stop()
        if self.action == "hit":
            self.frame += 1
            if self.frame < 20:
                vx,vy = self.vx,self.vy
                self.move(objgroup)
                self.vx,self.vy = vx,vy
            else:
                self.action = "stand"
        elif self.action == "attack":
            if self.frame > self.animecycle * self.imgobj.num - 1:
                self.action = "stop"
                self.frame = 0
        else:
            self.walk()
            self.stand()
            self.move(objgroup)
        self.animation(screen)
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

        
class MyBullet(Bullet):
    def __init__(self,x,y,width,height,atk,speed,time,
                 filename = None):
        Bullet.__init__(self,x,y,width,height,atk,speed,
                        time,filename)




                
