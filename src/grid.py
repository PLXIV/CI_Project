from cell import CellType, CellBuilding, CellRoad, CellSidewalk, CellEmpty
import random as rnd
from math import sqrt
from square import Square

# The grid represents the city blocks and streets
class Grid:

    # Build a grid of rows and columns with n intersections
    def __init__(self, rows, cols, n_intersections):
        assert(rows > 0)
        assert(cols > 0)
        self.rows = rows
        self.cols = cols
        self.n_intersections = n_intersections
        self.intersections = set()
        self.__cells = [[]]

    # Get a Cell from the grid
    def get(self, row, col):
        assert(len(self.__cells) == self.rows)
        assert(len(self.__cells[0]) == self.cols)
        assert(row < self.rows)
        assert(col < self.cols)
        return self.__cells[row][col]

    # Generates a random grid
    def generate(self, seed=None):
        if seed is not None:
            rnd.seed(seed)

        if self.n_intersections < 0:
            return

        rows = self.rows // 2
        cols = self.cols // 2

        # Create ROWSxCOLS matrix with default type building
        self.__cells = [[CellEmpty() for _ in range(cols)] for _ in range(rows)]
        self.intersections = set()

        # In order to create the streets a recursive subdivision of the grid is performed. At each iteration
        # in the while loop, the grid is subdivided in smaller squares horizontally or vertically (randomly selected)
        # creating intersections for the streets as follows: (X marks the intersections and * marks the roads)
        #
        # #1                    #2                    #3                    #5                    #6
        #   +-------------+       +------+------+       +------+------+       +------+------+       ...
        #   |             |       |      *      |       |      *      |       |      *      |
        #   |             |       |      *      |       |      *      |       |******X      |
        #   |             |       |      *      |       |      *      |       |      *      |
        #   |             |       |      *      |       |      X******+       |      X******|
        #   |             |       |      *      |       |      *      |       |      *      |
        #   +-------------+       +------+------+       +------+------+       +------+------+

        squares = [Square(row=0, col=0, w=(cols - 1), h=(rows - 1))]

        while len(self.intersections) < self.n_intersections:
            square = rnd.choice(squares)

            # If the square is not divisible into intersections, choose another one to subdivide
            if square.is_indivisible():
                continue

            # Subdivide the square
            A, B, corners = square.rand_subdivide()

            # Allow for intersections that overlap, but not intersections next to each other, if this last thing
            # happens, choose another square to subdivide
            d1 = self.__distance_to_nearest_intersection(corners[0])
            d2 = self.__distance_to_nearest_intersection(corners[1])
            if (d1 < 2 and d1 > 0) or (d2 < 2 and d2 > 0):
                continue

            # If the number of intersections surpass the limit, choose another square to subdivide
            new_intersections = self.intersections.copy()
            if not self.__is_border(corners[0]): new_intersections.add(corners[0])
            if not self.__is_border(corners[1]): new_intersections.add(corners[1])
            if len(self.intersections) > self.n_intersections:
                continue

            # Add the intersections and the subdivided square
            squares.remove(square)
            squares.append(A)
            squares.append(B)
            self.intersections = new_intersections

            # Build the roads for those new intersections
            self.__build_road(corners)

        self.__subdivide_grid()


    def __duplicate_elements(self, elements):
        new_elements = []
        for el in elements:
            new_elements.append(el)
            new_elements.append(el)
        return new_elements

    def __subdivide_grid(self):

        updated_cells = []
        for i, row in enumerate(self.__cells):
            new_row = [CellRoad() if cell.type == CellType.Road else CellEmpty() for cell in row]
            updated_cells.append(self.__duplicate_elements(row))
            updated_cells.append(self.__duplicate_elements(new_row))

        self.__cells = updated_cells


    def __is_border(self, corner):
        if corner[0] in [0, self.rows - 1]: return True
        if corner[1] in [0, self.cols - 1]: return True
        return False

    def __build_road(self, corners):
        x1 = corners[0][1] # Col 1
        x2 = corners[1][1] # Col 2
        y1 = corners[0][0] # Row 1
        y2 = corners[1][0] # Row 2

        if abs(y1 - y2) > 0:
            start = min([y1, y2])
            final = max([y1, y2]) + 1
            for y in range(start, final):
                self.__cells[y][x1] = CellRoad()
        else:
            start = min([x1, x2])
            final = max([x1, x2]) + 1
            for x in range(start, final):
                self.__cells[y1][x] = CellRoad()

    def __distance_to_nearest_intersection(self, intersection):
        min = float('+inf')
        for other in self.intersections:
            dx = other[0] - intersection[0]
            dy = other[1] - intersection[1]
            d = sqrt(dx ** 2 + dy ** 2)
            if d < min:
                min = d
        return min

    def __str__(self):
        txt = ""
        for row in self.__cells:
            for cell in row:
                txt += str(cell)
            txt += "\n"
        return txt
