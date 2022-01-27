import time as t
import pygame as pg

class Color:
    black = ( 25, 25, 25)
    white = (200,200,200)
    red   = (200, 25, 25)
    green = ( 25,200, 25)
    blue  = ( 25, 25,200)

class FrameRate:
    def __init__(self, target: int):
        self.fps = 0
        self.target = target
        self.reference = t.time()

    def cap(self):
        timesdelta = t.time() - self.reference

        if timesdelta < 1/self.target:
            t.sleep(1/self.target - timesdelta)

        self.fps = round(1/(t.time() - self.reference))
        self.reference = t.time()

class Task:
    def __init__(self, time_trigger, callback):
        self.callback = callback
        self.time_trigger = time_trigger
        self.time_reference = t.time()
    
    def update(self):
        timesdelta = t.time() - self.time_reference
        if timesdelta >= self.time_trigger:
            self.callback()
            self.time_reference = t.time()

def message():
    print('THE TIME HAS COME')

def print_fps():
    global framerate
    print(framerate.fps)

def move_thing():
    global thing
    global speed
    thing.x += speed
    if thing.x > 480:
        speed = -speed 
    elif thing.x < 0:
        speed = -speed 


game_exit = False

thing = pg.Rect(0,0,50,200)
speed = 1

render_list = [
    thing
]

tasks = [
    Task(10, message),
    Task(3, print_fps),
    Task(0.1, move_thing)
]

framerate = FrameRate(60)

pg.init()
pg.display.set_mode((640,480))

while not game_exit:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_exit = True

    for task in tasks:
        task.update()

    # Render
    surface = pg.display.get_surface()
    surface.fill(Color.black)

    for box in render_list:
        pg.draw.rect(surface, Color.red, box, width=1)

    pg.display.flip()

    # FPS Control
    framerate.cap()
pg.quit()