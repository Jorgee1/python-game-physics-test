import math
import time as t
import pygame as pg

class Color:
    black = ( 25, 25, 25)
    gray  = ( 30, 30, 30)
    white = (200,200,200)
    red   = (200, 25, 25)
    green = ( 25,200, 25)
    blue  = ( 25,100,200)

class Bool2:
    def __init__(self, x=False, y=False):
        self.x = x
        self.y = y

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

class Event:
    def __init__(self, id, collider, color):
        self.id = id
        self.collider = collider
        self.color = color

class Entity:
    def __init__(self, collider, max_speed, color):
        self.collider = collider
        self.speed = pg.Vector2()
        self.collision = Bool2()
        self.color = color
        self.max_speed = max_speed
    
    def update(self):
        self.collider.x += self.speed.x
        self.collider.y += self.speed.y

def draw_box(box: Box, color: Color):
    surface = pg.display.get_surface()
    pg.draw.rect(surface, color, box.rect, width=1)

def create_box(x, y, wall_w, wall_h):
    return [
        Entity(Box(x,y,wall_h,wall_w), 0, Color.green),
        Entity(Box(x,y,wall_w,wall_h), 0, Color.green),
        Entity(Box(x+wall_h-wall_w,y,wall_w,wall_h), 0, Color.green),
        Entity(Box(x,y+wall_h-wall_w,wall_h,wall_w), 0, Color.green)
    ]

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
wall_w = 20
game_exit = False


screen = Box(0,0,640,480)

map_id=1
# Map 1
box1 = create_box(10,50,20,400)
box1_start = pg.Vector2(160, 160)

# Map 2
box2 = create_box(100,100,20,300)
box2_start = pg.Vector2(200, 160)
wall1 = Entity(Box(249,300,40,40), 0, Color.green)

p1 = Entity(Box(box1_start.x,box1_start.y,40,40), 10, Color.red)

event1 = Event(1,Box(40,80,20,20), Color.blue)
event2 = Event(2,Box(150,250,20,20), Color.blue)

dynamic_list = []
event_list = []
static_list = []
render_list = []

transition = True
transition_start = False
transition_count = 0

pg.init()
pg.display.set_mode(screen.size)

while not game_exit:
    ref_time = t.time()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_exit = True
            break

    # Transition
    if transition:
        if map_id == 1:
            p1.collider.x = box1_start.x
            p1.collider.y = box1_start.y
            p1.speed.x = 0
            p1.speed.y = 0

            dynamic_list = [p1]
            event_list = [event1]
            static_list = [] + box1
            render_list = [p1, event1] + box1

        elif map_id == 2:
            p1.collider.x = box2_start.x
            p1.collider.y = box2_start.y
            p1.speed.x = 0
            p1.speed.y = 0

            dynamic_list = [p1]
            event_list = [event2]
            static_list = [wall1] + box2
            render_list = [p1, event2, wall1] + box2

        transition = False
    # Input
    keys = pg.key.get_pressed()

    if keys[pg.K_UP]:
        p1.speed.y = -p1.max_speed
    elif keys[pg.K_DOWN]:
        p1.speed.y = p1.max_speed
    else:
        p1.speed.y = 0

    if keys[pg.K_LEFT]:
        p1.speed.x = -p1.max_speed
    elif keys[pg.K_RIGHT]:
        p1.speed.x = p1.max_speed
    else:
        p1.speed.x = 0


    # Events
    for event in event_list:
        if check_collition(p1.collider, event.collider):
            if event.id == 1 and keys[pg.K_z]:
                transition_start = True
                map_id = 2
            if event.id == 2 and keys[pg.K_z]:
                transition_start = True
                map_id = 1

    # Collition
    for box in dynamic_list:
        box.collision.x = False
        box.collision.y = False
        speed_x = box.speed.x
        speed_y = box.speed.y
        for i in range(step+1):
            for wall in static_list:

                # Speed
                speed = pg.Vector2()
                speed.x = i*speed_x/step
                speed.y = i*speed_y/step

                f_speed = pg.Vector2()
                f_speed.x = (i+1)*speed_x/step
                f_speed.y = (i+1)*speed_y/step

                # Collider
                f_box = box.collider.copy()
                f_box.x += f_speed.x
                f_box.y += f_speed.y

                f_box_x = box.collider.copy()
                f_box_x.x += f_speed.x
                f_box_x.y += speed.y

                f_box_y = box.collider.copy()
                f_box_y.x += speed.x
                f_box_y.y += f_speed.y

                # Flags
                collision_x  = check_collition(f_box_x, wall.collider)
                collision_y  = check_collition(f_box_y, wall.collider)
                collision_xy = check_collition(f_box  , wall.collider)


                if collision_x and not collision_y:
                    box.collision.x = True
                    speed_x = speed.x
                    break

                if collision_y and not collision_x:
                    box.collision.y = True
                    speed_y = speed.y
                    break

                if collision_xy:
                    box.collision.x = True
                    box.collision.y = True
                    speed_x = (i-1)*speed_x/step
                    speed_y = (i-1)*speed_y/step
                    break
                    
        box.speed.x = speed_x
        box.speed.y = speed_y

    # Update
    if not transition_start:
        for box in dynamic_list:
            box.update()

    # Render
    surface = pg.display.get_surface()
    surface.fill(Color.black)

    for box in render_list:
        draw_box(box.collider, box.color)

    if transition_start:
        rect = pg.Rect(0,0,screen.w, transition_count * screen.h/30)
        pg.draw.rect(surface, Color.gray, rect)

    pg.display.flip()

    # FPS Control
    timestamp = t.time() - ref_time
    if timestamp < 1/(fps+0.5):
        t.sleep(1/(fps+0.5) - timestamp)
    
    if transition_start:
        if transition_count < 30:
            transition_count += 1
        elif transition_count >= 30:
            transition_count = 0
            transition_start = False
            transition = True
    
    print(round(1/(t.time() - ref_time)), transition_count)



pg.quit()

