from .box import Box

def check_x(A: Box, B: Box):
    return (A.x <= B.x + B.w) and (A.x + A.w >= B.x)

def check_y(A: Box, B: Box):
    return (A.y <= B.y + B.h) and (A.y + A.h >= B.y)

def check(A: Box, B: Box):
    return check_x(A, B) and check_y(A, B)

