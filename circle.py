import math
import time
import random as r
import pygame as pg

class Color:
    black = (25, 25, 25)
    white = (200, 200, 200)
    red = (200,100,100)
    blue = (100,200,100)


class Circle:
    def __init__(self, *, x, y, r, color):
        self.x = x
        self.y = y
        self.r = r
        self.color = color

        self.speed = pg.Vector2(0,0)

    @property
    def center(self):
        return pg.Vector2(self.x, self.y)

    @property
    def rect(self):
        return pg.Rect(
            self.x - self.r,
            self.y - self.r,
            self.r * 2,
            self.r * 2
        )

def draw_bound_rect(circle: Circle):
    surface = pg.display.get_surface()
    pg.draw.rect(surface, circle.color, circle.rect, width=1)

def draw_circle(circle: Circle):
    surface = pg.display.get_surface()
    pg.draw.circle(surface, circle.color, circle.center, circle.r, width=1)

def check_circle_collition(c1, c2):
    return math.dist(c1.center, c2.center) < c1.r + c2.r


width = 640
height = 480
n_circle = 50
step = 10
game_exit = False



p1 = Circle(x=100, y=100, r=100, color=Color.red)

render_list = [p1]

for i in range(n_circle):
    x = r.random() * (width - 100) + 50
    y = r.random() * (height - 100) + 50

    if round(r.random()):
        x = -1*x

    if round(r.random()):
        y = -1*y

    speed_x = r.random()
    speed_y = math.sqrt(1-speed_x**2)
    circle = Circle(x=x, y=y, r=50, color=Color.blue)
    circle.speed.x = speed_x * 10
    circle.speed.y = speed_y * 10
    render_list.append(circle)

pg.init()
pg.display.set_mode((width, height))

while not game_exit:
    ref_time = time.time()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_exit = True

    # Input
    keys = pg.key.get_pressed()

    if keys[pg.K_LEFT]:
        p1.speed.x = -5
    elif keys[pg.K_RIGHT]:
        p1.speed.x = 5
    else:
        p1.speed.x = 0

    if keys[pg.K_UP]:
        p1.speed.y = -5
    elif keys[pg.K_DOWN]:
        p1.speed.y = 5
    else:
        p1.speed.y = 0


    # Collition detection
    for c in render_list[1:]:
        temp_speed_x = c.speed.x
        temp_speed_y = c.speed.y
        for i in range(1, step+1):
            temp_p = Circle(x=p1.x, y=p1.y, r=p1.r, color=Color.white)
            temp_p.x = p1.x + i*p1.speed.x/step
            temp_p.y = p1.y + i*p1.speed.y/step

            temp_c = Circle(x=c.x, y=c.y, r=c.r, color=Color.white)
            temp_c.x = c.x + i*c.speed.x/step
            temp_c.y = c.y + i*c.speed.y/step

            if check_circle_collition(temp_p, temp_c):
                # Reverse the vector consistenly?
                temp_speed_x = -temp_p.x + temp_c.x
                temp_speed_y = -temp_p.y + temp_c.y

                mag = math.sqrt(temp_speed_x**2 + temp_speed_y**2)

                temp_speed_x = 10*temp_speed_x/mag
                temp_speed_y = 10*temp_speed_y/mag
                break

            # Screen colition
            if c.x - c.r + i*c.speed.x/step < 0:
                temp_speed_x = abs(c.speed.x)

            if c.y - c.r + i*c.speed.y/step < 0:
                temp_speed_y = abs(c.speed.y)

            if c.x + c.r + i*c.speed.x/step > width:
                temp_speed_x = -abs(c.speed.x)

            if c.y + c.r + i*c.speed.y/step > height:
                temp_speed_y = -abs(c.speed.y)

        c.speed.x = temp_speed_x
        c.speed.y = temp_speed_y
            


    # Update
    for c in render_list:
        c.x += c.speed.x
        c.y += c.speed.y

    # Renderer
    surface = pg.display.get_surface()
    surface.fill(Color.black)

    for c in render_list:
        draw_circle(c)
        #draw_bound_rect(c)

    pg.display.flip()


    timestamp = time.time() - ref_time
    if timestamp < 1/60:
        time.sleep((1/60) - timestamp)

    print(round(1/(time.time() - ref_time)))

pg.quit()