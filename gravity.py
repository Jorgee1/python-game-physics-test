import math
import time as t
import random as r
import pygame as pg

class Color:
    black = (25, 25, 25)
    white = (200, 200, 200)
    red = (200, 25, 25)
    green = (25, 200, 25)
    blue = (25, 25, 200)

class Box:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def copy(self):
        return Box(self.x, self.y, self.w, self.h)

    @property
    def center(self):
        return pg.Vector2(self.x + self.w/2, self.y + self.h/2)

    @property
    def rect(self):
        return pg.Rect(self.x, self.y, self.w, self.h)

class Entity:
    def __init__(self, collider: Box, color: Color):
        self.collider = collider
        self.speed = pg.Vector2()
        self.color = color

    def update(self):
        self.collider.x += self.speed.x
        self.collider.y += self.speed.y

def draw_box(box: Box, color: Color):
    surface = pg.display.get_surface()
    pg.draw.rect(surface, color, box.rect, width=1)

def check_collition(A: Box, B: Box):
    # A Edges
    A_IZQ = A.x
    A_DER = A.x + A.w
    A_ARR = A.y
    A_ABJ = A.y + A.h

    # B Edges
    B_IZQ = B.x
    B_DER = B.x + B.w
    B_ARR = B.y
    B_ABJ = B.y + B.h

    # Restrictions

    return (
        (A_ABJ >= B_ARR) and (A_ARR <= B_ABJ) and
        (A_DER >= B_IZQ) and (A_IZQ <= B_DER)
    )



width  = 640
height = 480
step = 10
fps = 60
n = 10
gravity = 13
game_exit = False


boxes = []

for i in range(n):
    entity = Entity(Box(i*width/n,0,20,10), Color.red)
    boxes.append(entity)

boxes_static = [Entity(Box(0,height - 100,width,5), Color.green)]

pg.init()
pg.display.set_mode((width, height))

while not game_exit:
    ref_time = t.time()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_exit = True

    # Apply Force
    for box in boxes:
        box.speed.y += gravity

    # Collition Detection
    for box_static in boxes_static:
        for box in boxes:
            for i in range(step):

                temp_box = box.collider.copy()
                temp_box.x += i*box.speed.x/step
                temp_box.y += i*box.speed.y/step

                if check_collition(temp_box, box_static.collider):
                    box.speed.y = (i-1)*box.speed.y/step
                    break

    # Update
    for box in boxes:
        box.update()

    # Render
    surface = pg.display.get_surface()
    surface.fill(Color.black)

    for box in boxes_static:
        draw_box(box.collider, box.color)

    for box in boxes:
        draw_box(box.collider, box.color)


    pg.display.flip()

    timestamp = t.time() - ref_time
    if timestamp < 1/fps:
        t.sleep(1/fps - timestamp)

    print(round(1/(t.time() - ref_time)))

pg.quit()