import math
import time as t
import random as r
import pygame as pg

class Color:
    black = ( 25, 25, 25)
    white = (200,200,200)
    red   = (200, 25, 25)
    green = ( 25,200, 25)
    blue  = ( 25, 25,200)

class Box:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    @property
    def rect(self):
        return pg.Rect(self.x, self.y, self.w, self.h)
    
    @property
    def size(self):
        return (self.w, self.h)

fps = 60
game_exit = False
screen = Box(0,0,640,480)

pg.init()
pg.display.set_mode(screen.size)

while not game_exit:
    ref_time = t.time()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_exit = True

    surface = pg.display.get_surface()
    surface.fill(Color.black)
    pg.display.flip()

    timestamp = t.time() - ref_time
    if timestamp < 1/fps:
        t.sleep(1/fps - timestamp)

    print(round(1/(t.time() - ref_time)))

pg.quit()