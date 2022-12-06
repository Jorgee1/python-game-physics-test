import math, time, pygame as pg
from random import random

from utils.general import Colors
from utils.circle import Circle, draw_circle, check_circle_collition


width = 640
height = 480
n_circle = 50
step = 50
game_exit = False


p1 = Circle(x=100, y=100, r=100, color=Colors.red)

circles = [p1]

for i in range(n_circle):
    x = random() * (width - 100) + 50
    y = random() * (height - 100) + 50

    if round(random()):
        x = -1*x

    if round(random()):
        y = -1*y

    speed_x = random()
    speed_y = math.sqrt(1-speed_x**2)
    circle = Circle(x=x, y=y, r=50, color=Colors.green)
    circle.speed.x = speed_x * 10
    circle.speed.y = speed_y * 10
    circles.append(circle)

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
    for c in circles[1:]:
        temp_speed_x = c.speed.x
        temp_speed_y = c.speed.y
        for i in range(1, step+1):
            temp_p = Circle(x=p1.x, y=p1.y, r=p1.r, color=Colors.white)
            temp_p.x = p1.x + i*p1.speed.x/step
            temp_p.y = p1.y + i*p1.speed.y/step

            temp_c = Circle(x=c.x, y=c.y, r=c.r, color=Colors.white)
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
    for c in circles:
        c.x += c.speed.x
        c.y += c.speed.y

    # Renderer
    surface = pg.display.get_surface()
    surface.fill(Colors.black)

    for c in circles:
        draw_circle(c)

    pg.display.flip()


    timestamp = time.time() - ref_time
    if timestamp < 1/60:
        time.sleep((1/60) - timestamp)

    print(round(1/(time.time() - ref_time)))

pg.quit()





