import math
import random as r
import time as t
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
    blue  = ( 25,100,200)

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
    def __init__(self, box, color):
        self.collider = box
        self.speed = pg.Vector2()
        self.color = color
        self.collision = Bool2()
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

n = 20
fps = 60
step = 3
game_exit = False

screen = Box(0,0,640,480)

p1 = Entity(Box(0,0,50,50), Color.red)
p1.collider.x = screen.w/2 - p1.collider.w/2
p1.collider.y = screen.h/2 - p1.collider.h/2


wall1 = Entity(Box(40,40,100,100), Color.green)

wall2 = Entity(Box(0,0,10,screen.h*2), Color.green)
wall3 = Entity(wall2.collider.copy(), Color.green)
wall3.collider.x = screen.w*2 - wall3.collider.w

wall4 = Entity(Box(0,0,screen.w*2,10), Color.green)
wall5 = Entity(wall4.collider.copy(), Color.green)
wall5.collider.y = screen.h*2 - wall5.collider.h

wall6 = Entity(Box(400,400,200,200), Color.green)

wall7 = Entity(Box(1000,600,200,200), Color.green)
wall8 = Entity(Box(1050,50,200,200), Color.green)

wall9 = Entity(Box(50,800,200,100), Color.green)

dynamic_list = [p1]
static_list = [wall1, wall2, wall3, wall4, wall5, wall6, wall7, wall8, wall9]
render_list = [p1, wall1, wall2, wall3, wall4, wall5, wall6, wall7, wall8, wall9]


for i in range(n):
    dummy = Entity(Box(20+i*55,330,50,50), Color.blue)

    dummy.speed.x = (1+r.random())*2*(-1)**i
    dummy.speed.y = (1+r.random())*2*(-1)**i


    dynamic_list.append(dummy)
    render_list.append(dummy)


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
        p1.speed.y = -10
    elif keys[pg.K_DOWN]:
        p1.speed.y = 10
    else:
        p1.speed.y = 0

    if keys[pg.K_LEFT]:
        p1.speed.x = -10
    elif keys[pg.K_RIGHT]:
        p1.speed.x = 10
    else:
        p1.speed.x = 0

    # Colition
    for box in dynamic_list:
        box.collision.x = False
        box.collision.y = False
        for wall in static_list:
            for i in range(1, step+1):
                f_box = box.collider.copy()
                f_box.x += i*box.speed.x/step
                f_box.y += i*box.speed.y/step

                f_box_x = box.collider.copy()
                f_box_x.x += i*box.speed.x/step
                f_box_x.y += (i-1)*box.speed.y/step

                f_box_y = box.collider.copy()
                f_box_y.x += (i-1)*box.speed.x/step
                f_box_y.y += i*box.speed.y/step

                colition_x = check_collition(f_box_x, wall.collider)
                colition_y = check_collition(f_box_y, wall.collider)
                colition_xy = check_collition(f_box, wall.collider)

                if colition_x and not colition_y:
                    box.collision.x = True
                    box.speed.x = (i-1)*box.speed.x/step
                    break

                if colition_y and not colition_x:
                    box.collision.y = True
                    box.speed.y = (i-1)*box.speed.y/step
                    break

                if colition_xy:
                    box.collision.x = True
                    box.collision.y = True
                    box.speed.x = (i-1)*box.speed.x/step
                    box.speed.y = (i-1)*box.speed.y/step
                    break


    # Update
    for box in dynamic_list:
        box.update()

    screen.x = p1.collider.x + p1.collider.w/2 - screen.w/2
    screen.y = p1.collider.y + p1.collider.h/2 - screen.h/2

    # Render
    surface = pg.display.get_surface()
    surface.fill(Color.black)

    for box in render_list:
        render_box = box.collider.copy()
        render_box.x -= screen.x
        render_box.y -= screen.y
        draw_box(render_box, box.color)

    pg.display.flip()

    # FPS Control
    timestamp = t.time() - ref_time
    if timestamp < 1/(fps + 0.5):
        t.sleep(1/(fps+0.5) - timestamp)
    
    print(round(1/(t.time() - ref_time)))

pg.quit()