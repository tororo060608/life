#!/usr/bin/env python

import pygame
from pygame.locals import *


def load_map(filename):
    map = []
    fp = open(filename,"r")
    for line in fp:
        line = line.rstrip()
        map.append(list(line))
    fp.close()
    return map


