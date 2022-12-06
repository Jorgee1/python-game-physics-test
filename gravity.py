import math, pygame as pg
from time import time, sleep
from utils.general import Colors, check_box_collition

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
    def __init__(self, collider: Box, color: tuple):
        self.collider = collider
        self.speed = pg.Vector2()
        self.color = color

    def update(self):
        self.collider.x += self.speed.x
        self.collider.y += self.speed.y

def draw_box(box: Box, color: tuple):
    surface = pg.display.get_surface()
    pg.draw.rect(surface, color, box.rect, width=1)


def set_fps(fps, ref_time):
    timestamp = time() - ref_time
    if 1/fps > timestamp: sleep(1/fps - timestamp)
    return time()

width = 640
height = 480
step = 10
frame_limit = 60
n = 10
gravity = 1
game_exit = False


boxes = [Entity(Box(i*width/n, 0, 20, 10), Colors.red) for i in range(n)]

boxes_static = [Entity(Box(0, height-100, width, 5), Colors.green)]

pg.init()
pg.display.set_mode((width, height))

ref_time = time()

while not game_exit:
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_exit = True

    # Apply Force
    for box in boxes: box.speed.y += gravity

    # Collition Detection
    for current_box in boxes_static:
        for box in boxes:
            for i in range(step):

                future_box = box.collider.copy()
                future_box.x += i*box.speed.x/step
                future_box.y += i*box.speed.y/step

                if check_box_collition(future_box, current_box.collider):
                    box.speed.y = (i-1)*box.speed.y/step
                    break

    # Update
    for box in boxes: box.update()

    # Render
    surface = pg.display.get_surface()
    surface.fill(Colors.black)

    for box in boxes_static:
        draw_box(box.collider, box.color)

    for box in boxes:
        draw_box(box.collider, box.color)

    pg.display.flip()

    # FPS Control
    ref_time = set_fps(frame_limit, ref_time)


pg.quit()
