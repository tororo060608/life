#!/usr/bin/env python

import pygame
from pygame.locals import *
import math

import obj

class MyChara(obj.Chara):
    def __init__(self,imagedict,x,y,hp,atk,defe,speed,stamina):
        obj.Chara.__init__(self,imagedict,x,y,hp,atk,defe,speed)
        self.stamina = stamina
        self.weapon_wide = 64
        self.weapon_length = 32
        self.bullettime = 12

    def attack(self):
        if self.action == "hit": return
        if self.action not in ["attack","stop"]:
            self.frame = 0
            self.action = "attack"

    def make_bullet(self):
        if self.frame >= 12:
            if self.dire == "left":
                MyBullet(self.x - self.weapon_length,
                         self.y-(self.weapon_wide - self.height) /2,
                         self.weapon_length,
                         self.weapon_wide,
                         self.atk,0,self.bullettime)
            if self.dire == "right":
                MyBullet(self.x + self.weapon_length,
                         self.y-(self.weapon_wide - self.height) /2,
                         self.weapon_length,
                         self.weapon_wide,
                         self.atk,0,self.bullettime)
            if self.dire == "front":
                MyBullet(self.x-(self.weapon_wide - self.width) / 2,
                         self.y + self.height,
                         self.weapon_wide,
                         self.weapon_length,
                         self.atk,0,self.bullettime)
            if self.dire == "back":
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
        elif self.action == "hit" or self.invincibletime:
            self.invincibletime += 1
            return
        for enemy in enemys:
            collide = self.rect.colliderect(enemy)
            if collide:
                self.action = "hit"
                self.frame = 0
                self.invincibletime += 1
                dmg = self.damage(enemy)
                self.hp -= dmg
                dx = enemy.rect.centerx - self.rect.centerx
                dy = enemy.rect.centery - self.rect.centery
                rad = math.atan2(dy,dx)
                self.vx = - self.speed * math.cos(rad) * 1.5
                self.vy = - self.speed * math.sin(rad) * 1.5
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

    def hit_bullet(self,blts):
        pass

    def move(self,objgroup):
        if self.action == "hit":
            if self.frame < 10:
                vx,vy = self.vx,self.vy
                obj.Chara.move(self,objgroup)
                self.vx,self.vy = vx,vy
            else:
                self.action = "stand"
        else:
            obj.Chara.move(self,objgroup)
                
    def update(self,screen,enemygroup):
        self.hit_enemy(enemygroup)
        self.stop()
        if self.action == "hit":
            pass
        elif self.action == "attack":
            self.make_bullet()
            if self.frame > 35:
                self.action = "stop"
                self.frame = 0
        else:
            self.walk()
            self.stand()
        obj.Chara.update(self,screen)


class MyBullet(obj.Bullet):
    def __init__(self,x,y,width,height,atk,speed,time,
                 filename = None):
        obj.Bullet.__init__(self,x,y,width,height,atk,speed,
                        time,filename)
