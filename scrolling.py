import math
import time as t
import random as r
import pygame as pg

class Bool2:
    def __init__(self, x=False, y=False):
        self.x = x
        self.y = y

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
    
    def copy(self):
        return Box(self.x, self.y, self.w, self.h)

    @property
    def rect(self):
        return pg.Rect(self.x, self.y, self.w, self.h)
    
    @property
    def size(self):
        return (self.w, self.h)

class Entity:
    def __init__(self, collider: Box, color: Color):
        self.collider = collider
        self.collision = Bool2()
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
speed_limit = 20
speed_lock_left = False
speed_lock_right = False
game_exit = False
jump_lock = False
screen = Box(0,40,640,480)

p1 = Entity(Box(100,100,50,50), Color.red)
floor = Entity(Box(0,0,2*screen.w,40), Color.green)
floor.collider.y = screen.h - floor.collider.h

floor1 = Entity(Box(0,0,10,screen.h), Color.green)

floor3 = Entity(Box(400,0,200,60), Color.green)
floor3.collider.y = floor.collider.y - floor3.collider.h

floor4 = Entity(Box(0,0,200,20), Color.green)
floor4.collider.x = floor.collider.x + floor.collider.w + 200
floor4.collider.y = floor.collider.y - 50

dynamic_list = [p1]
static_list = [floor, floor1, floor3, floor4]
render_list = [p1, floor, floor1, floor3, floor4]

pg.init()
pg.display.set_mode(screen.size)

while not game_exit:
    ref_time = t.time()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_exit = True
            break

    keys = pg.key.get_pressed()
    
    # Input

    if keys[pg.K_UP]:
        if p1.collision.y and not jump_lock:
            p1.speed.y += -40
            jump_lock = True
    else:
        jump_lock = False

    if keys[pg.K_LEFT]:
        if not speed_lock_left:
            p1.speed.x = 0
        p1.speed.x -= 1
        if p1.speed.x < -speed_limit:
            p1.speed.x = -speed_limit
        speed_lock_left = True
    elif keys[pg.K_RIGHT]:
        if not speed_lock_right:
            p1.speed.x = 0
        p1.speed.x += 1
        if p1.speed.x > speed_limit:
            p1.speed.x = speed_limit
        speed_lock_right = True
    else:
        p1.speed.x = 0

    if not keys[pg.K_LEFT]:
        speed_lock_left = False

    if not keys[pg.K_RIGHT]:
        speed_lock_right = False

    # Apply Force
    for box in dynamic_list:
        box.speed.y += gravity 

    # Collision

    if p1.collider.y > 10000: # Return to stage
        p1.collider.x = screen.w/2 - p1.collider.w/2
        p1.collider.y = 0
        p1.speed.y = 0

    for box in dynamic_list:
        box.collision.x = False
        box.collision.y = False
        for wall in static_list:
            for i in range(1, step+1):
                f_box = box.collider.copy()
                f_box.x += i*box.speed.x/step
                f_box.y += i*box.speed.y/step

                if check_collition(f_box, wall.collider):
                    f_box_x = box.collider.copy()
                    f_box_x.x += i*box.speed.x/step
                    f_box_x.y += (i-1)*box.speed.y/step

                    f_box_y = box.collider.copy()
                    f_box_y.x += (i-1)*box.speed.x/step
                    f_box_y.y += i*box.speed.y/step

                    if check_collition(f_box_x, wall.collider):
                        box.collision.x = True
                        box.speed.x = (i-1)*box.speed.x/step
                        
                    if check_collition(f_box_y, wall.collider):
                        box.collision.y = True
                        box.speed.y = (i-1)*box.speed.y/step

                    break

    # Update
    for box in dynamic_list:
        box.update()

    screen.x = p1.collider.x + p1.collider.w/2 - screen.w/2
    #screen.y = p1.collider.y + p1.collider.h/2 - screen.h/2

    # Render
    surface = pg.display.get_surface()
    surface.fill(Color.black)

    for box in render_list:
        temp_box = box.collider.copy()
        temp_box.x -= screen.x
        temp_box.y -= screen.y
        draw_box(temp_box, box.color)

    pg.display.flip()

    timestamp = t.time() - ref_time
    if timestamp < 1/(fps+0.5):
        timestamp1 = t.time() - ref_time
        t.sleep(1/(fps+0.5) - timestamp1)

    print(round(1/(t.time() - ref_time)))

pg.quit()