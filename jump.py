import math
import time as t
import random as r
import pygame as pg

class Color:
    black = ( 25,  25,  25)
    white = (200, 200, 200)
    red   = (200,  25,  25)
    green = ( 25, 150,  25)
    blue  = ( 100,  150, 200)

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
        self.colision_x = False
        self.colision_y = False

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
cap_fps = True
step = 10
gravity = 4
game_exit = False

speed_limit_x = 10
jump_lock = False
speed_lock_left = False
speed_lock_right = False
screen = Box(0,0,640,480)

player = Entity(Box(100,0,50,50), Color.red)
thing = Entity(Box(450,0,50,50), Color.blue)
thing_sign = 1

floor = Entity(Box(0,0, screen.w, 100), Color.green)
floor.collider.y = screen.h - floor.collider.h

floor2 = Entity(Box(0,0,100,100), Color.green)
floor2.collider.x = 300
floor2.collider.y = screen.h - floor2.collider.h - floor.collider.h

floor3 = Entity(Box(0,0,10,screen.h), Color.green)
floor4 = Entity(Box(screen.w-10,0,10,screen.h), Color.green)

dynamic_list = [player, thing]
static_list = [floor, floor2, floor3, floor4]
render_list = [player, floor, floor2, floor3, floor4, thing]



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
        if player.colision_y and not jump_lock:
            player.speed.y = -40
            jump_lock = True
    elif not keys[pg.K_UP]:
        jump_lock = False

    if keys[pg.K_LEFT]:
        if not speed_lock_left:
            player.speed.x = 0
        player.speed.x += -2
        if player.speed.x < -speed_limit_x:
            player.speed.x = -speed_limit_x
        
        speed_lock_left = True
    elif keys[pg.K_RIGHT]:
        if not speed_lock_right:
            player.speed.x = 0
        
        player.speed.x += 2
        if player.speed.x > speed_limit_x:
            player.speed.x = speed_limit_x

        speed_lock_right = True
    else:
        player.speed.x = 0

    if not keys[pg.K_LEFT]:
        speed_lock_left = False

    if not keys[pg.K_RIGHT]:
        speed_lock_right = False

    # Apply Force
    thing.speed.x = thing_sign * 5


    for box in dynamic_list:
        box.speed.y += gravity

    # Collition Static
    for dbox in dynamic_list:
        dbox.colision_x = False
        dbox.colision_y = False
        for sbox in static_list:
            for i in range(1, step+1):
                f_dbox = dbox.collider.copy()
                f_dbox.x += i*dbox.speed.x/step
                f_dbox.y += i*dbox.speed.y/step
                
                f_sbox = sbox.collider.copy()
                #f_sbox.x += i*sbox.speed.x/step
                #f_sbox.y += i*sbox.speed.y/step

                if check_collition(f_sbox, f_dbox):

                    f_dbox_x = dbox.collider.copy()
                    f_dbox_x.x += i*dbox.speed.x/step
                    f_dbox_x.y += (i-1)*dbox.speed.y/step

                    f_dbox_y = dbox.collider.copy()
                    f_dbox_y.x += (i-1)*dbox.speed.x/step
                    f_dbox_y.y += i*dbox.speed.y/step

                    if check_collition(f_sbox, f_dbox_x):
                        dbox.speed.x = (i-1)*dbox.speed.x/step
                        dbox.colision_x = True
                        
                    if check_collition(f_sbox, f_dbox_y):
                        dbox.speed.y = (i-1)*dbox.speed.y/step
                        dbox.colision_y = True

                    break

    # Update
    if thing.colision_x:
        thing_sign = -thing_sign

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
    if (timestamp < 1/fps) and cap_fps:
        t.sleep(1/fps - timestamp)
    
    print(round(1/(t.time() - ref_time)))
pg.quit()

