from pygame import Rect, draw
from pygame.display import get_surface
from pygame.math import Vector2

class Box:
    def __init__(self, x: float, y: float, w: float, h: float):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def copy(self):
        return Box(self.x, self.y, self.w, self.h)

    @property
    def rect(self):
        return Rect(
            round(self.x),
            round(self.y),
            round(self.w),
            round(self.h)
        )

    @property
    def center(self):
        x = (self.x + self.x + self.w)/2
        y = (self.y + self.y + self.h)/2
        return Vector2(x, y)

    @property
    def size(self):
        return (self.w, self.h)


def draw_box(box: Box, color: (int, int, int)):
    surface = get_surface()
    draw.rect(surface, color, box.rect)

