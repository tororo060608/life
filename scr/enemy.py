#!/usr/bin/env python

import pygame
from pygame.locals import *
import math

import obj
import random


class Enemy(obj.Chara):
    def __init__(self,imagedict,x,y,hp,atk,defe,speed):
        obj.Chara.__init__(self,imagedict,x,y,hp,atk,defe,speed)
        self.searcharea = 200
        self.searchrect = pygame.Rect(self.rect.centerx - self.searcharea / 2,
                                      self.rect.centery - self.searcharea / 2,
                                      self.searcharea,
                                      self.searcharea)
        
    def search_enemy(self,targetgroup):
        tgt = None
        min = 1000000000
        self.searchrect = pygame.Rect(self.rect.centerx - self.searcharea / 2,
                                      self.rect.centery - self.searcharea / 2,
                                      self.searcharea,
                                      self.searcharea)
        for target in targetgroup:
            collide = self.searchrect.colliderect(target.rect)
            if collide:
                distance = (self.rect.centerx-target.rect.centerx)^2+(self.rect.centery-target.rect.centery)^2
                if distance < min:
                    tgt = target
                    min = distance
        if min < 100:
            self.action = "attack"
        elif tgt and min >= 100:
            self.action = "walk"
        return tgt

    def move(self,objgroup,targetgroup):
        target = self.search_enemy(targetgroup)
        if target and self.action == "walk":
            x = self.rect.centerx - target.rect.centerx
            y = self.rect.centery - target.rect.centery
            rad = math.atan2(y,x)
            self.vx = self.speed * math.cos(rad)
            self.vy = self.speed * math.sin(rad)
            if math.fabs(x) > math.fabs(y):
                if x > 0:
                    self.dire = "right"
                elif x < 0:
                    self.dire = "left"
            elif math.fabs(x) < math.fabs(y):
                if y > 0:
                    self.dire = "front"
                elif y < 0:
                    self.dire = "back"
            obj.Chara.move(objgroup)

    def update(self,screen,objgroup,targetgroup):
        self.animation(screen)
        self.move(objgroup,targetgroup)
        self.frame += 1

class Boar(Enemy):
    def __init__(self,imagedict,x,y,hp,atk,defe,speed):
        Enemy.__init__(self,imagedict,x,y,hp,atk,defe,speed)

    def move(self,objgroup,targetgroup):
        if self.action == "stop": return
        target = self.search_enemy(targetgroup)
        if target and self.action == "walk":
            dx = self.rect.centerx - target.rect.centerx
            dy = self.rect.centery - target.rect.centery
            rad = math.atan2(dy,dx)
            self.vx = - self.speed * math.cos(rad)
            self.vy = - self.speed * math.sin(rad)
        if target and self.action == "attack":
            dx = self.rect.centerx - target.rect.centerx
            dy = self.rect.centery - target.rect.centery
            rad = math.atan2(dy,dx)
            self.vx = - self.speed * math.cos(rad) * 2
            self.vy = - self.speed * math.sin(rad) * 2
        
        if math.fabs(self.vx) >= math.fabs(self.vy):
            if self.vx > 0:
                self.dire = "right"
            elif self.vx < 0:
                self.dire = "left"
        elif math.fabs(self.vx) < math.fabs(self.vy):
            if self.vy > 0:
                self.dire = "front"
            elif self.vy < 0:
                self.dire = "back"
        obj.Chara.move(self,objgroup)

    def hit_enemy(self,enemys):
        for enemy in enemys:
            collide = self.rect.colliderect(enemy.rect)
            if collide:
                self.action = "stop"
                self.frame = 0
                
    def stop(self):
        if self.action == "stop" and self.frame > 10:
            self.action = "stand"
            self.frame = 0

    def update(self,screen,objgroup,targetgroup):
        self.hit_enemy(targetgroup)
        self.stop()
        self.animation(screen)
        self.move(objgroup,targetgroup)
        self.frame += 1
        
