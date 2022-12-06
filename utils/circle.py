import math
import pygame as pg

class Circle:
    def __init__(self, *, x, y, r, color):
        self.x = x
        self.y = y
        self.r = r
        self.color = color

        self.speed = pg.Vector2(0, 0)

    @property
    def center(self):
        return pg.Vector2(self.x, self.y)

    @property
    def rect(self):
        return pg.Rect(
            self.x - self.r,
            self.y - self.r,
            self.r * 2,
            self.r * 2
        )

def draw_circle(circle: Circle):
    surface = pg.display.get_surface()
    pg.draw.circle(surface, circle.color, circle.center, circle.r, width=1)

def check_circle_collition(c1, c2):
    return math.dist(c1.center, c2.center) < c1.r + c2.r