
import json

from pathlib import Path

from pygame.time import Clock
from pygame.math import Vector2
from pygame import init, event, QUIT
from pygame.display import set_mode, get_surface, flip

from lib.box import Box, draw_box
from lib.controller import Controller
from lib import color as Color, collision



class Bool2:
    def __init__(self, x=False, y=False):
        self.x = x
        self.y = y

class Entity:
    def __init__(self, x=0, y=0, w=0, h=0, color=Color.black, airborn=False):
        self.collider = Box(x, y, w, h)
        self.collision = Bool2()
        self.speed = Vector2()
        self.color = color
        self.airborn = airborn
        self.jump_counter = 0

    def update(self):
        self.collider.x += self.speed.x
        self.collider.y += self.speed.y

        self.jump_counter -= 1
        if self.jump_counter <= 0:
            self.jump_counter = 0

class Warp:
    def __init__(self, x=0, y=0, w=0, h=0, color=Color.black, destination=''):
        self.collider = Box(x, y, w, h)
        self.color = color
        self.destination = destination


def load_level(level_path):
    # TODO: Exceptions?
    # Maybe parse game objects here instead that on lists later?
    with open(level_path) as f:
        data = json.load(f)
    
    return data['name'], data


def main():
    root = Path(__file__).parent

    target_fps = 60
    steps = 10
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

    init()
    set_mode(screen.size)
    clock = Clock()
    
    controls = Controller()

    while not game_exit:

        for e in event.get():
            if e.type == QUIT:
                game_exit = True
                break

        controls.update()

        # Input TODO: implement movement schema
        if controls.accept.press:
            if not p1.airborn:
                p1.airborn = True
                p1.jump_counter = 8


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

            if box.airborn:
                if box.jump_counter:
                    box.speed.y += -8

        # Collision

        if p1.collider.y > 10000: # Return to stage
            p1.collider.x = screen.w/2 - p1.collider.w/2
            p1.collider.y = 0
            p1.speed.y = 0

        for box in dynamic_list:
            box.collision.x = False
            box.collision.y = False
            for wall in static_list:

                future_player = p1.collider.copy()
                future_player.x += box.speed.x
                future_player.y += box.speed.y

                if collision.check(future_player, wall.collider):
                    for i in range(steps):
                        prev_player = p1.collider.copy()
                        prev_player.x += i * box.speed.x / steps
                        prev_player.y += i * box.speed.y / steps

                        next_player = p1.collider.copy()
                        next_player.x += (i + 1) * box.speed.x / steps
                        next_player.y += (i + 1) * box.speed.y / steps

                        current_x = collision.check_x(prev_player, wall.collider)
                        current_y = collision.check_y(prev_player, wall.collider)

                        future_x = collision.check_x(next_player, wall.collider)
                        future_y = collision.check_y(next_player, wall.collider)

                        if future_x and not current_x:
                            box.collision.x = True
                            box.speed.x = i * box.speed.x / steps
                            break

                        if future_y and not current_y:
                            box.collision.y = True
                            box.speed.y = i * box.speed.y / steps

                            b_center = box.collider.center
                            w_center = wall.collider.center

                            if (b_center.y < w_center.y):
                                print('land feet')
                                p1.airborn = False
                            else:
                                print('bump head')
                                p1.airborn = True

                            p1.jump_counter = 0
                            break

            if not box.collision.y:
                box.airborn = True

        for box in warps:
            if collision.check(p1.collider, box.collider):
                next_level = box.destination

        # Update
        for box in dynamic_list:
            box.update()

        screen.x = p1.collider.x + p1.collider.w/2 - screen.w/2
        #screen.y = p1.collider.y + p1.collider.h/2 - screen.h/2

        # Render
        surface = get_surface()
        surface.fill(Color.black)

        for box in render_list:
            temp_box = box.collider.copy()
            temp_box.x -= screen.x
            temp_box.y -= screen.y
            draw_box(temp_box, box.color)

        flip()

        if next_level:
            data   = levels[next_level]
            p1     = Entity(**data['player'], airborn=p1.airborn)
            floors = [Entity(**i) for i in data['walls']]
            warps  = [Warp(**i) for i in data['warp']]

            dynamic_list = [p1]
            static_list = floors
            render_list = dynamic_list + floors + warps
            next_level = None

        clock.tick(target_fps)
main()