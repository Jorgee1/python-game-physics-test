from pygame.time import Clock
from pygame.math import Vector2
from pygame import init, event, QUIT
from pygame.display import set_mode, get_surface, flip

from lib.box import Box, draw_box
from lib import color as Color
from lib import collision
from lib.controller import Controller

class Entity:
    def __init__(self, collider, color):
        self.collider = collider
        self.speed = Vector2()
        self.color = color
        self.colision_x = False
        self.colision_y = False

    def update(self):
        self.collider.x += self.speed.x
        self.collider.y += self.speed.y

target_fps = 60
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

floor5 = Entity(Box(0,225,100,10), Color.green)


dynamic_list = [player, thing]
static_list = [floor, floor2, floor3, floor4, floor5]
render_list = dynamic_list + static_list



init()
set_mode(screen.size)
clock = Clock()

controls = Controller()

while not game_exit:
    for e in event.get():
        if e.type == QUIT:
            game_exit = True

    # Input
    controls.update()

    if controls.up.state:
        if player.colision_y and not jump_lock:
            player.speed.y = -40
            jump_lock = True
    elif not controls.up.state:
        jump_lock = False

    if controls.left.state:
        if not speed_lock_left:
            player.speed.x = 0
        player.speed.x += -2
        if player.speed.x < -speed_limit_x:
            player.speed.x = -speed_limit_x
        
        speed_lock_left = True
    elif controls.right.state:
        if not speed_lock_right:
            player.speed.x = 0
        
        player.speed.x += 2
        if player.speed.x > speed_limit_x:
            player.speed.x = speed_limit_x

        speed_lock_right = True
    else:
        player.speed.x = 0

    if not controls.left.state:
        speed_lock_left = False

    if not controls.right.state:
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

                f_dbox_x = dbox.collider.copy()
                f_dbox_x.x += i*dbox.speed.x/step
                f_dbox_x.y += (i-1)*dbox.speed.y/step

                f_dbox_y = dbox.collider.copy()
                f_dbox_y.x += (i-1)*dbox.speed.x/step
                f_dbox_y.y += i*dbox.speed.y/step

                colition_x = collision.check(f_dbox_x, sbox.collider)
                colition_y = collision.check(f_dbox_y, sbox.collider)
                colition_xy = collision.check(f_dbox, sbox.collider)



                if colition_x and not colition_y:
                    dbox.colision_x = True
                    dbox.speed.x = (i-1)*dbox.speed.x/step
                    break

                if colition_y and not colition_x:
                    dbox.colision_y = True
                    dbox.speed.y = (i-1)*dbox.speed.y/step
                    break

                """
                if colition_xy:
                    dbox.colision_x = True
                    dbox.colision_y = True
                    dbox.speed.x = (i-1)*dbox.speed.x/step
                    dbox.speed.y = (i-1)*dbox.speed.y/step
                    break
                """
    # Update
    if thing.colision_x:
        thing_sign = -thing_sign

    for box in dynamic_list:
        box.update()

    # Render
    surface = get_surface()
    surface.fill(Color.black)
    
    for box in render_list:
        draw_box(box.collider, box.color)

    flip()

    # FPS Control
    clock.tick(target_fps)
