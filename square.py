import time as t
import pygame as pg
import random as r

class Color:
    black = (25,   25,  25)
    white = (200, 200, 200)
    red   = (200, 100, 100)
    blue  = (100, 100, 200)

class Box:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    @property
    def center(self):
        return pg.Vector2(self.x + self.w/2, self.y + self.h/2)

    def __repr__(self):
        return f'<{round(self.x, 2)}, {round(self.y, 2)}>'

    def to_rect(self):
        return pg.Rect(self.x, self.y, self.w, self.h)

class Entity:
    def __init__(self, collider: Box, color=Color.white):
        self.collider = collider
        self.color = color
        self.speed = pg.Vector2()

    def update(self):
        self.collider.x += self.speed.x
        self.collider.y += self.speed.y

def draw_box(box: Box, color):
    surface = pg.display.get_surface()
    pg.draw.rect(surface, color, box.to_rect(), width=1)

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


width = 640
height = 480
n_boxes = 1000
game_exit = False

pg.init()
pg.display.set_mode((640, 480))

player = Entity(Box(100,100,100,100), Color.red)

boxes = [player]

for i in range(n_boxes):
    x = r.random() * (width - 40)
    y = r.random() * (height - 40)
    box = Box(x, y, 40, 40)
    entity = Entity(box, Color.blue)
    entity.speed.y = 1
    boxes.append(entity)


while not game_exit:
    ref_time = t.time()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_exit = True

    # Input
    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT] and keys[pg.K_RIGHT]:
        player.speed.x = 0
    elif keys[pg.K_LEFT]:
        player.speed.x = -5
    elif keys[pg.K_RIGHT]:
        player.speed.x = 5
    else:
        player.speed.x = 0

    if keys[pg.K_UP] and keys[pg.K_DOWN]:
        player.speed.y = 0
    if keys[pg.K_UP]:
        player.speed.y = -5
    elif keys[pg.K_DOWN]:
        player.speed.y = 5
    else:
        player.speed.y = 0

    for box in boxes[1:]:
        if check_collition(player.collider, box.collider):
            box.color = Color.blue
        else:
            box.color = Color.white

        if box.collider.y < 0:
            box.speed.y = -box.speed.y

        if box.collider.y + box.collider.h > height:
            box.speed.y = -box.speed.y
    # Update
    for box in boxes:
        box.update()

    # Render
    surface = pg.display.get_surface()
    surface.fill(Color.black)

    for box in reversed(boxes):
        draw_box(box.collider, box.color)

    pg.display.flip()

    frame_time = t.time() - ref_time
    if frame_time < 1/60:
        t.sleep(1/60 - frame_time)

    print(round(1/(t.time() - ref_time)))

pg.quit()

