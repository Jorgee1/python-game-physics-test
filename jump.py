import math
import time as t
import random as r
import pygame as pg

class Color:
    black = ( 25,  25,  25)
    white = (200, 200, 200)
    red   = (200,  25,  25)
    green = ( 25, 200,  25)
    blue  = ( 25,  25, 200)


class Box:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def copy(self):
        return Box(self.x, self.y, self.w, self.h)

    @property
    def rect(self):
        return pg.Rect(self.x, self.y, self.w, self.h)

    @property
    def size(self):
        return (self.w, self.h)

class Entity:
    def __init__(self, collider, color):
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



fps = 60
step = 10
gravity = 5
game_exit = False
screen = Box(0,0,640,480)

player = Entity(Box(100,100,50,50), Color.red)
floor = Entity(Box(0,0, screen.w, 100), Color.green)
floor.collider.y = screen.h - floor.collider.h

floor2 = Entity(Box(0,0, 100, 100), Color.green)
floor2.collider.x = screen.w - floor2.collider.w
floor2.collider.y = screen.h - floor2.collider.h - floor.collider.h

dynamic_list = [player]
static_list = [floor, floor2]
render_list = [player, floor, floor2]



pg.init()
pg.display.set_mode(screen.size)

while not game_exit:
    ref_time = t.time()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_exit = True

    # Input
    keys = pg.key.get_pressed()

    if keys[pg.K_UP]:
        if player.speed.y == 0:
            player.speed.y = -40

    if keys[pg.K_LEFT]:
        player.speed.x = -10
    elif keys[pg.K_RIGHT]:
        player.speed.x = 10
    else:
        player.speed.x = 0

    # Apply Force
    player.speed.y += gravity

    # Collition
    for sbox in static_list:
        for dbox in dynamic_list:
            for i in range(step):
                f_dbox = dbox.collider.copy()
                f_dbox.x += i*dbox.speed.x/step
                f_dbox.y += i*dbox.speed.y/step
                
                f_sbox = sbox.collider.copy()
                f_sbox.x += i*sbox.speed.x/step
                f_sbox.y += i*sbox.speed.y/step

                if check_collition(f_sbox, f_dbox):
                    
                    f_dbox = dbox.collider.copy()
                    f_dbox.x += i*dbox.speed.x/step
                    f_dbox.y += (i-1)*dbox.speed.y/step

                    if check_collition(f_sbox, f_dbox):
                        dbox.speed.x = (i-1)*dbox.speed.x/step

                    f_dbox = dbox.collider.copy()
                    f_dbox.x += (i-1)*dbox.speed.x/step
                    f_dbox.y += i*dbox.speed.y/step

                    if check_collition(f_sbox, f_dbox):
                        dbox.speed.y = (i-1)*dbox.speed.y/step


                    break

    # Update
    for box in dynamic_list:
        box.update()

    # Render
    surface = pg.display.get_surface()
    surface.fill(Color.black)
    
    for box in render_list:
        draw_box(box.collider, box.color)

    pg.display.flip()

    # FPS Control
    timestamp = t.time() - ref_time
    if (timestamp < 1/fps):
        t.sleep(1/fps - timestamp)
    
    print(round(1/(t.time() - ref_time)), player.speed.y)
pg.quit()

