import random as rnd
from enum import Enum
from cell import Orientation

class Square:
    MIN_DIST = 2 # Minimum distance between the border of the square and the division line

    def __init__(self, row, col, w, h):
        self.row = row
        self.col = col
        self.w = w
        self.h = h

    def __get_corners(self):
        return \
            [(self.row, self.col),
             (self.row, self.col + self.w),
             (self.row + self.h, self.col + self.w),
             (self.row + self.h, self.col)]

    def __subdivide_vertical(self, h):
        A = Square(row=self.row, col=self.col, w=self.w, h=h)
        B = Square(row=self.row + h, col=self.col, w=self.w, h=self.h - h)
        cornersA = set(A.__get_corners())
        cornersB = set(B.__get_corners())
        return A, B, list(cornersA.intersection(cornersB)), Orientation.Horizontal

    def __subdivide_horizontal(self, w):
        A = Square(row=self.row, col=self.col, w=w, h=self.h)
        B = Square(row=self.row, col=self.col + w, w=self.w - w, h=self.h)
        cornersA = set(A.__get_corners())
        cornersB = set(B.__get_corners())
        return A, B, list(cornersA.intersection(cornersB)), Orientation.Vertical

    def is_indivisible(self):
        return (self.h - 2 * self.MIN_DIST) <= 0 and (self.w - 2 * self.MIN_DIST) <= 0

    def rand_subdivide(self):
        if (self.h - 2 * self.MIN_DIST) <= 0:
            w = rnd.randint(self.MIN_DIST, self.w - self.MIN_DIST)
            return self.__subdivide_horizontal(w)
        if (self.w - 2 * self.MIN_DIST) <= 0:
            h = rnd.randint(self.MIN_DIST, self.h - self.MIN_DIST)
            return self.__subdivide_vertical(h)

        subdivide_direction = rnd.choice([Orientation.Horizontal, Orientation.Vertical])

        if  subdivide_direction == Orientation.Horizontal:
            h = rnd.randint(self.MIN_DIST, self.h - self.MIN_DIST)
            return self.__subdivide_vertical(h)
        else:
            w = rnd.randint(self.MIN_DIST, self.w - self.MIN_DIST)
            return self.__subdivide_horizontal(w)
