#!/usr/bin/env python

import pygame
from pygame.locals import *
import sys

import game

def main():
    pygame.init()
    pygame.display.set_caption("life")

    clock = pygame.time.Clock()
    
    while True:
        clock.tick(60)
        game.game.screen.fill((0,0,0))
        game.game.update()
        pygame.display.update()    


main()
