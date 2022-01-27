import time as t
import pygame as pg
from utils.general import Colors

pg.init()

fps = 60
scale = 3
game_exit = False
clock = pg.time.Clock()

world_base = pg.image.load('assets/farm.png')
rect = world_base.get_clip()
rect.w *= scale
rect.h *= scale
world = pg.transform.scale(world_base, (rect.w, rect.h))
pg.display.set_mode((640,480))

while not game_exit:

    # Events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_exit = True

    # Input
    keys = pg.key.get_pressed()


    # Render
    surface = pg.display.get_surface()
    surface.fill(Colors.black)

    surface.blit(world, (0,0))

    pg.display.flip()

    # Frame Control
    clock.tick(fps)

pg.quit()