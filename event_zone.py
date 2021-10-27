import math
import time as t
import random as r
import pygame as pg

class Color:
    black = ( 25, 25, 25)
    gray  = (100,100,100)
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
    def center(self):
        return pg.Vector2(self.x + self.w/2, self.y + self.h/2)

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

class Zone:
    def __init__(self, id, collider, color):
        self.id = id
        self.collider = collider
        self.color = color

def draw_box(box: Box, color: Color):
    surface = pg.display.get_surface()
    pg.draw.rect(surface, color, box.rect, width=1)

def check_collition(A: Box, B: Box):
    # AABB
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

n = 6
fps = 60
step = 10
game_exit = False
event_trigger = False
screen = Box(0,0,640,480)

p1 = Entity(Box(0,0,50,50), Color.red)
p1.collider.x = p1.collider.x - p1.collider.w/2 + screen.w/2 
p1.collider.y = p1.collider.y - p1.collider.h/2 + screen.h/2

wall1 = Entity(Box(0,0,screen.w, 10), Color.green)
wall2 = Entity(Box(0,0,10, screen.h), Color.green)
wall3 = Entity(Box(0,0,screen.w, 10), Color.green)
wall3.collider.y = screen.h - wall3.collider.h
wall4 = Entity(Box(0,0,10, screen.h), Color.green)
wall4.collider.x = screen.w - wall4.collider.w

zone1 = Zone(0, Box(0,0,50,50), Color.blue)
zone1.collider.x = 10 + (r.random()*(screen.w-zone1.collider.w-20))
zone1.collider.y = 10 + (r.random()*(screen.h-zone1.collider.h-20))

zone_list = [zone1]
for i in range(len(zone_list), n):
    zone = Zone(i, Box(0,0,50,50), Color.blue)
    zone.collider.x = 10 + (r.random()*(screen.w-zone.collider.w-20))
    zone.collider.y = 10 + (r.random()*(screen.h-zone.collider.h-20))
    zone_list.append(zone)

dynamic_list = [p1]
static_list = [wall1, wall2, wall3, wall4]
render_list = [p1, wall1, wall2, wall3, wall4]

pg.init()
pg.display.set_mode(screen.size)

while not game_exit:
    ref_time = t.time()

    # Event
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_exit = True

    # Input
    keys = pg.key.get_pressed()

    event_trigger = keys[pg.K_z]

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

    # Collition

    for zone in zone_list:
        zone.color = Color.blue
        if check_collition(p1.collider, zone.collider):
            if event_trigger:
                zone.color = Color.gray
                
            if zone.id == 0 and event_trigger:
                print("Is dangerous to go alone, take this")
            elif zone.id == 1:
                p1_c = p1.collider.center
                z_c = zone.collider.center

                v_x = p1_c.x - z_c.x
                v_y = p1_c.y - z_c.y
                mag = math.sqrt(v_x**2 + v_y**2)

                p1.speed.x = 100*v_x/mag
                p1.speed.y = 100*v_y/mag
            elif event_trigger:
                print("Nothing to do here")
            break

    for box in dynamic_list:
        for wall in static_list:
            test_box = box.collider.copy()
            test_box.x += box.speed.x
            test_box.y += box.speed.y

            if not check_collition(test_box, wall.collider):
                # If the box is not going to collide with anything
                # there is no need to keep checking for dynamic vs static
                continue

            for i in range(1, step+1):
                f_box = box.collider.copy()
                f_box.x += i*box.speed.x/step
                f_box.y += i*box.speed.y/step
                colition_xy = check_collition(f_box, wall.collider)

                f_box = box.collider.copy()
                f_box.x += i*box.speed.x/step
                f_box.y += (i-1)*box.speed.y/step
                colition_x = check_collition(f_box, wall.collider)

                f_box = box.collider.copy()
                f_box.x += (i-1)*box.speed.x/step
                f_box.y += i*box.speed.y/step
                colition_y = check_collition(f_box, wall.collider)


                if colition_x and not colition_y:
                    box.speed.x = (i-1)*box.speed.x/step
                    break

                if colition_y and not colition_x:
                    box.speed.y = (i-1)*box.speed.y/step
                    break

                if colition_xy:
                    box.speed.x = (i-1)*box.speed.x/step
                    box.speed.y = (i-1)*box.speed.y/step
                    break

    # Update

    for box in dynamic_list:
        box.update()

    # Render
    surface = pg.display.get_surface()
    surface.fill(Color.black)

    for box in render_list:
        draw_box(box.collider, box.color)

    for zone in zone_list:
        draw_box(zone.collider, zone.color)

    pg.display.flip()

    # FPS Control
    timestamp = t.time() - ref_time
    if timestamp < 1/(fps + 0.5):
        t.sleep(1/(fps+0.5) - timestamp)

    print(round(1/(t.time() - ref_time)))

pg.quit()

