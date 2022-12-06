import math
import time as t
import random as r
import pygame as pg
import json

from pathlib import Path

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
    def __init__(self, x=0, y=0, w=0, h=0, color=Color.black):
        self.collider = Box(x, y, w, h)
        self.collision = Bool2()
        self.speed = pg.Vector2()
        self.color = color

    def update(self):
        self.collider.x += self.speed.x
        self.collider.y += self.speed.y

class Warp:
    def __init__(self, x=0, y=0, w=0, h=0, color=Color.black, destination=''):
        self.collider = Box(x, y, w, h)
        self.color = color
        self.destination = destination

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
            self.accept,
            self.refect
        ]

    def update(self):
        keys = pg.key.get_pressed()
        
        for key in self.keys:
            key.update(keys)


def draw_box(box: Box, color: Color):
    surface = pg.display.get_surface()
    pg.draw.rect(surface, color, box.rect)

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

def load_level(level_path):
    # TODO: Exceptions?
    # Maybe parse game objects here instead that on lists later?
    with open(level_path) as f:
        data = json.load(f)
    
    return data['name'], data
    

def main():
    root = Path(__file__).parent

    fps = 60
    step = 10
    gravity = 5
    speed_limit = 20
    speed_lock_left = False
    speed_lock_right = False
    game_exit = False
    jump_lock = False
    next_level = None


    screen = Box(0, 0, 640, 480)
    levels = {k: v for k, v in map(load_level, (root / 'levels').iterdir())}
    
    data   = levels['level1']
    p1     = Entity(**data['player'])
    floors = [Entity(**i) for i in data['walls']]
    warps  = [Warp(**i) for i in data['warp']]

    dynamic_list = [p1]
    static_list = floors
    render_list = dynamic_list + floors + warps

    pg.init()
    pg.display.set_mode(screen.size)
    
    ref_time = t.time()

    controls = Controller()


    while not game_exit:
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_exit = True
                break

        keys = pg.key.get_pressed()
        controls.update()
        print(controls.accept.state)

        # Input
        if controls.accept.state:
            if not jump_lock:
                p1.speed.y += -8

                if p1.speed.y < -30:
                    jump_lock = True
        else:
            if p1.speed.y == 0:
                jump_lock = False
            else:
                jump_lock = True

        if controls.left.state:
            if not speed_lock_left:
                p1.speed.x = 0
            p1.speed.x -= 1
            if p1.speed.x < -speed_limit:
                p1.speed.x = -speed_limit
            speed_lock_left = True
        elif controls.right.state:
            if not speed_lock_right:
                p1.speed.x = 0
            p1.speed.x += 1
            if p1.speed.x > speed_limit:
                p1.speed.x = speed_limit
            speed_lock_right = True
        else:
            p1.speed.x = 0

        if not controls.left.state:
            speed_lock_left = False

        if not controls.right.state:
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

        for box in warps:
            if check_collition(p1.collider, box.collider):
                next_level = box.destination

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

        if next_level:
            data   = levels[next_level]
            p1     = Entity(**data['player'])
            floors = [Entity(**i) for i in data['walls']]
            warps  = [Warp(**i) for i in data['warp']]

            dynamic_list = [p1]
            static_list = floors
            render_list = dynamic_list + floors + warps
            next_level = None

        timestamp = t.time() - ref_time
        if timestamp < 1/(fps):
            timestamp1 = t.time() - ref_time
            t.sleep(1/(fps) - timestamp1)

        #print(round(1/(t.time() - ref_time)))
        ref_time = t.time()


    pg.quit()



main()