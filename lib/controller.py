from math import sqrt

import pygame as pg
from pygame.math import Vector2
class Key:
    def __init__(self, key):
        self.id = key
        self.state = False
        self.press = False

        self.press_lock = False

    def update(self, keys):
        value = keys[self.id]
        self.state = value

        if not self.press_lock:
            self.press = True
            self.press_lock = True
        else:
            self.press = False

        if not value:
            self.press = False
            self.press_lock = False

class Controller:
    def __init__(self):
        self.up    = Key(pg.K_UP)
        self.left  = Key(pg.K_LEFT)
        self.right = Key(pg.K_RIGHT)
        self.down  = Key(pg.K_DOWN)
        
        self.accept = Key(pg.K_z)
        self.refect = Key(pg.K_x)

        self.keys = [
            self.up,
            self.left,
            self.right,
            self.down,
            self.accept,
            self.refect
        ]

    @property
    def movement(self):
        movement = Vector2()

        if self.up.state:
            movement.y = -1.0
        elif self.down.state:
            movement.y = 1.0
        else:
            movement.y = 0.0

        if self.left.state:
            movement.x = -1.0
        elif self.right.state:
            movement.x = 1.0
        else:
            movement.x = 0.0

        if movement.x and movement.y:
            movement.x = sqrt(2) * movement.x / 2
            movement.y = sqrt(2) * movement.y / 2

        return movement


    def update(self):
        keys = pg.key.get_pressed()
        
        for key in self.keys:
            key.update(keys)


