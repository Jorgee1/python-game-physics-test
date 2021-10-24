import math
import time as t
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

dynamic_list = [p1]
static_list = [wall1, wall2, wall3, wall4, wall5, wall6]
render_list = [p1, wall1, wall2, wall3, wall4, wall5, wall6]

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
        for wall in static_list:
            f_box = box.collider.copy()
            f_box.x += box.speed.x
            f_box.y += box.speed.y
            if check_collition(f_box, wall.collider):
                box.speed.x = 0
                box.speed.y = 0

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