import yaml
import pygame as pg

class Color:
    black = ( 25,  25,  25)
    gray  = ( 50,  50,  50)
    white = (200, 200, 200)
    red   = (200,  25,  25)
    green = ( 25, 150,  25)
    blue  = (100, 150, 200)


game_exit = False
grid = 16*1

pg.init()
pg.display.set_mode((1280, 720))

p_start = None
p_end = None
save_rect = False
rects = []

world_base = pg.image.load('assets/farm.png')
rect = world_base.get_clip()
rect.w *= 1
rect.h *= 1
world = pg.transform.scale(world_base, (rect.w, rect.h))

while not game_exit:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_exit = True

    b_left, _, _ = pg.mouse.get_pressed()
    mouse_position = pg.Vector2(pg.mouse.get_pos())
    mouse_position.x -= mouse_position.x % grid
    mouse_position.y -= mouse_position.y % grid

    if b_left:
        if p_start == None:
            p_start = pg.Vector2(mouse_position)
            select_rect = pg.Rect(0,0,0,0)
            rects.append(select_rect)

        if p_start != None:
            p_end = pg.Vector2(mouse_position)
            p_end.x += grid
            p_end.y += grid

        if p_start.x < p_end.x:
            select_rect.x = p_start.x
            select_rect.w = abs(p_end.x - p_start.x)
        else:
            select_rect.x = p_end.x - grid
            select_rect.w = abs(p_end.x - p_start.x) + 2*grid

        if p_start.y < p_end.y:
            select_rect.y = p_start.y
            select_rect.h = abs(p_end.y - p_start.y)
        else:
            select_rect.y = p_end.y - grid
            select_rect.h = abs(p_end.y - p_start.y) + 2*grid

        save_rect = True
    
    if save_rect and not b_left:
        p_start = None
        p_end = None
        save_rect = False
        
        

    surface = pg.display.get_surface()
    surface.fill(Color.black)
    surface.blit(world, (0,0))
    for rect in rects:
        pg.draw.rect(surface, Color.red, rect)
        pg.draw.rect(surface, Color.gray, rect, width=1)

    pg.draw.rect(surface, Color.white, (mouse_position.x, mouse_position.y, grid, grid))
    pg.display.flip()
pg.quit()

