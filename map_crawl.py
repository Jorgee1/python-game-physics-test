import time as t
import pygame as pg

class Color:
    black = (25,25,25)
    grey  = (40,40,40)
    white = (200,200,200)
    red   = (200,100,25)
    green = (25,200,25)
    blue  = (25,100,200)

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

class Warp:
    def __init__(self, id, collider: Box, color):
        self.id = id
        self.spawn = pg.Vector2()
        self.collider = collider
        self.color = color

class Entity:
    def __init__(self, collider, max_speed, color):
        self.collider = collider
        self.speed = pg.Vector2()
        self.max_speed = max_speed
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

def create_box(x, y, wall_w, wall_h):
    return [
        Entity(Box(x,y,wall_w,wall_h), 0, Color.green),
        Entity(Box(x,y,wall_h,wall_w), 0, Color.green),
        Entity(Box(x,y+wall_w-wall_h,wall_w,wall_h), 0, Color.green),
        Entity(Box(x+wall_w-wall_h,y,wall_h,wall_w), 0, Color.green)
    ]

fps = 60
step = 10
game_exit = False
transition = True
screen = Box(0,0,640,480)


p1 = Entity(Box(0,0,40,40), 5, Color.red)

event_list = []
dynamic_list = []
static_list = []
render_list = []

map_id = 1
# MAP 1
map1 = create_box(640/2-150,480/2-150,300,10)
start1 = pg.Vector2(640/2-20,480/2+50)
event1 = Warp(1,Box(640/2-10,480/2-150+20,20,20), Color.blue)
event1.spawn.x = 640/2 - p1.collider.w/2
event1.spawn.y = event1.collider.y + event1.collider.h + 10

# Map2
start2 = pg.Vector2(640/2,480/2)
map2 = create_box(640/2-200,480/2-200,400,10)
event2 = Warp(2,Box(640/2-10,480/2-200+20,20,20), Color.blue)
event2.spawn.x = 640/2 - p1.collider.w/2
event2.spawn.y = event2.collider.y + event2.collider.h + 10
event4 = Warp(4,Box(640/2-10,480/2+200-40,20,20), Color.blue)
event4.spawn.x = 640/2 - p1.collider.w/2
event4.spawn.y = event4.collider.y - event4.collider.h - p1.collider.h

# Map3
start3 = pg.Vector2(200,200)
map3 = create_box(640/2-150,480/2-150,300,10)
event3 = Warp(3,Box(640/2-10,480/2+ 150 - 40,20,20), Color.blue)
event3.spawn.x = 640/2 - p1.collider.w/2
event3.spawn.y = event3.collider.y - event3.collider.h - p1.collider.h
block = Entity(Box(640/2-90,480/2-90,40,40),0, Color.green)

pg.init()
pg.display.set_mode(screen.size)

while not game_exit:
    ref_time = t.time()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_exit = True

    # Map Transition
    if transition:
        if map_id == 1:
            p1.collider.x = start1.x
            p1.collider.y = start1.y
            p1.speed = pg.Vector2()

            event_list = [event1]
            dynamic_list = [p1]
            static_list = map1
            render_list = dynamic_list + static_list + event_list
            transition = False
        elif map_id == 2:
            p1.collider.x = start2.x
            p1.collider.y = start2.y
            p1.speed = pg.Vector2()

            event_list = [event2, event4]
            dynamic_list = [p1]
            static_list = map2
            render_list = dynamic_list + static_list + event_list
            transition = False
        elif map_id == 3:
            p1.collider.x = start3.x
            p1.collider.y = start3.y
            p1.speed = pg.Vector2()

            event_list = [event3]
            dynamic_list = [p1]
            static_list = map3 + [block]
            render_list = dynamic_list + static_list + event_list
            transition = False
        else:
            map_id = 1



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
                transition = True
                map_id = 2
                start1 = event1.spawn
                start2 = event4.spawn
            elif event.id == 2 and keys[pg.K_z]:
                transition = True
                map_id = 3
                start2 = event2.spawn
                start3 = event3.spawn
            elif event.id == 3 and keys[pg.K_z]:
                transition = True
                map_id = 2
            elif event.id == 4 and keys[pg.K_z]:
                transition = True
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
    for box in dynamic_list:
        box.update()

    # Render
    surface = pg.display.get_surface()
    surface.fill(Color.black)

    for box in render_list:
        draw_box(box.collider, box.color)

    pg.display.flip()

    timestamp = t.time() - ref_time
    if timestamp < 1/(fps+0.5):
        t.sleep(1/(fps+0.5) - timestamp)

    print(round(1/(t.time() - ref_time)))

pg.quit()
