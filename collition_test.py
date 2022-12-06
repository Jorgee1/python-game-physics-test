from pygame.time import Clock
from pygame.math import Vector2
from pygame import init, event, QUIT
from pygame.display import flip, set_mode, get_surface

from lib import color, collision
from lib.box import Box, draw_box
from lib.controller import Controller

def main():
    speed = 5
    target_fps = 60
    steps = 10
    game_exit = False

    controls = Controller()

    screen = Box(0.0, 0.0, 640.0, 480.0)
    player = Box(0.0, 0.0, 50.0, 50.0)

    walls = [
        Box(100.0, 100.0, 50.0, 50.0),
        Box(232.0, 219.0, 53.0, 56.0)
    ]

    player_speed = Vector2()

    init()
    set_mode(screen.size)
    clock = Clock()

    while not game_exit:
        for e in event.get():
            if e.type == QUIT:
                game_exit = True
                break
        
        controls.update()
        movement = controls.movement

        player_speed.x = speed * movement.x
        player_speed.y = speed * movement.y

        # Check if there will be a collision in the future
        # There will be tunneling of the player moves faster than its size

        for wall in walls:
            future_player = player.copy()
            future_player.x += player_speed.x
            future_player.y += player_speed.y

            if collision.check(future_player, wall):
                for i in range(steps):
                    prev_player = player.copy()
                    prev_player.x += i * player_speed.x / steps
                    prev_player.y += i * player_speed.y / steps

                    next_player = player.copy()
                    next_player.x += (i + 1) * player_speed.x / steps
                    next_player.y += (i + 1) * player_speed.y / steps

                    current_x = collision.check_x(prev_player, wall)
                    current_y = collision.check_y(prev_player, wall)

                    future_x = collision.check_x(next_player, wall)
                    future_y = collision.check_y(next_player, wall)

                    if future_x and not current_x:
                        player_speed.x = i * player_speed.x / steps
                        break

                    if future_y and not current_y:
                        player_speed.y = i * player_speed.y / steps
                        break


        # Update player position after collision
        player.x += player_speed.x
        player.y += player_speed.y

        surface = get_surface()
        surface.fill(color.black)

        for wall in walls:
            draw_box(wall, color.green)
        
        draw_box(player, color.white)


        flip()
        clock.tick(target_fps)

main()
