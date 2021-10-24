import time as t
import pygame as pg
import collections as c

game_exit = False

frames = c.deque()
fps = 60
limit = 400

pg.init()
pg.display.set_mode((640, 480))
min_frame = 100

while not game_exit:
    ref_time = t.time()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_exit = True
            break


    
    surface = pg.display.get_surface()
    surface.fill((25,25,25))

    temp_frames = list(frames)
    if temp_frames:
        if min_frame < min(temp_frames):
            min_frame = min(temp_frames)
        
    for i, v in enumerate(zip(temp_frames[:-1], temp_frames[1:])):
        v1, v2 = v
        v1 = (v1 - min_frame) * 15
        v2 = (v2 - min_frame) * 15
        pg.draw.line(surface, (200,25,25), (v1+50,i),(v2+50,i+1))

    pg.display.flip()

    timestamp = t.time() - ref_time
    if timestamp < 1/(fps+0.5):
        t.sleep(1/(fps+0.5) - timestamp)


    print(round(1/(t.time() - ref_time)))

    if len(frames) >= limit:
        frames.popleft()
        
    frames.append( (t.time() - ref_time) * 10000)
pg.quit()