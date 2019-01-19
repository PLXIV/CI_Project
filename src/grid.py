from cell import CellType, CellBuilding, CellRoad, CellSidewalk, CellEmpty, Direction
import random as rnd
from math import sqrt
from square import Square
from bfs import generate_bfs_dictionaries
from square import Orientation

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
        self.spawn_roads = []
        self.despawn_roads = []
        self.destinations = {}

    # Get a Cell from the grid
    def get(self, row, col):
        assert(len(self.__cells) == self.rows)
        assert(len(self.__cells[0]) == self.cols)
        assert(row < self.rows)
        assert(col < self.cols)
        return self.__cells[row][col]

    def generate(self, seed=None):
        if seed is not None:
            rnd.seed(seed)

        if self.n_intersections < 0:
            return

        max_iters = self.n_intersections * 2
        while not self.__generate_try(max_iters):
            seed = rnd.randint(1, 99999)
            print('Can not create map, retrying... seed={:d}'.format(seed))
            rnd.seed(seed)

    # Generates a random grid
    def __generate_try(self, max_iters=0):
        rows = self.rows // 2
        cols = self.cols // 2

        # Create ROWSxCOLS matrix with default type building
        self.__cells = [[CellEmpty(row, col) for col in range(cols)] for row in range(rows)]
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

        iters = 0
        while len(self.intersections) < self.n_intersections:
            # Check if there are too many iterations, a.k.a we are stuck
            iters += 1
            if 0 < max_iters < iters:
                return False

            # Choose a square to subdivide
            square = rnd.choice(squares)

            # If the square is not divisible into intersections, choose another one to subdivide
            if square.is_indivisible():
                continue

            # Subdivide the square
            A, B, corners, direction = square.rand_subdivide()

            # Allow for intersections that overlap, but not intersections next to each other, if this last thing
            # happens, choose another square to subdivide
            d1 = self.__distance_to_nearest_intersection(corners[0])
            d2 = self.__distance_to_nearest_intersection(corners[1])
            if (d1 < 2 and d1 > 0) or (d2 < 2 and d2 > 0):
                continue

            # If the number of intersections surpass the limit, choose another square to subdivide
            new_intersections = self.intersections.copy()
            if not self.__is_border(corners[0], rows, cols): new_intersections.add(corners[0])
            if not self.__is_border(corners[1], rows, cols): new_intersections.add(corners[1])
            if len(self.intersections) > self.n_intersections:
                continue

            # Add the intersections and the subdivided square
            squares.remove(square)
            squares.append(A)
            squares.append(B)
            self.intersections = new_intersections

            # Build the roads for those new intersections
            self.__build_road(corners, direction)

        self.__subdivide_grid()
        self.__setup_directions()
        self.__setup_road_connections()
        self.__cover_cells(cellToCover=CellType.Road, cellClass=CellSidewalk)
        self.__cover_cells(cellToCover=CellType.Sidewalk, cellClass=CellBuilding)
        self.__generate_crosswalks()
        self.__generate_sidewalk_connections()
        self.__set_spawn_roads()
        self.__set_despawn_roads()
        generate_bfs_dictionaries(self)
        return True

    def __set_spawn_roads(self):
        self.spawn_roads = []
        for row in self.__cells:
            for cell in row:
                if cell.type == CellType.Road and len(cell.parents) == 0:
                    self.spawn_roads.append(cell)

    def __set_despawn_roads(self):
        self.despawn_roads = []
        for row in self.__cells:
            for cell in row:
                if cell.type == CellType.Road and len(cell.children) == 0:
                    self.despawn_roads.append(cell)

    def __generate_sidewalk_connections(self):
        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.__cells[i][j]
                if cell.type == CellType.Sidewalk:
                    if (i + 1) < self.rows and self.__cells[i + 1][j].type == CellType.Sidewalk: cell.addChild(self.__cells[i + 1][j])
                    if (i - 1) >= 0        and self.__cells[i - 1][j].type == CellType.Sidewalk: cell.addChild(self.__cells[i - 1][j])
                    if (j + 1) < self.cols and self.__cells[i][j + 1].type == CellType.Sidewalk: cell.addChild(self.__cells[i][j + 1])
                    if (j - 1) >= 0        and self.__cells[i][j - 1].type == CellType.Sidewalk: cell.addChild(self.__cells[i][j - 1])

    def __generate_crosswalks(self):
        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.__cells[i][j]
                if cell.type == CellType.Road:
                    neighbours = self.__get_road_neighbours(i, j)
                    singles = self.__get_single_orientation(neighbours)
                    cell.hasCrosswalk = len(neighbours) > len(singles)
                    # cell.hasLights = len(neighbours) > len(singles)
                    cell.hasLights = 0
                    for child in cell.children:
                        if len(child.orientation) > 1:
                            cell.hasLights = 1


    def __cover_cells(self, cellToCover, cellClass):
        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.__cells[i][j]
                if cell.type == cellToCover:
                    # Check if above the road is empty, if it is insert a Sidewalk
                    if i != self.rows - 1:
                        if self.__cells[i+1][j].type == CellType.Empty:
                            self.__cells[i+1][j] = cellClass(i, j)
                    #Check if below the road is empty, if it is insert a Sidewalk
                    if i != 0:
                        if self.__cells[i-1][j].type == CellType.Empty:
                            self.__cells[i-1][j] = cellClass(i, j)
                    #Check if the right position the road is empty, if it is insert a Sidewalk
                    if j != self.cols - 1:
                        if self.__cells[i][j+1].type == CellType.Empty:
                            self.__cells[i][j+1] = cellClass(i, j)
                    #Check if the left position the road is empty, if it is insert a Sidewalk
                    if j != 0:
                        if self.__cells[i][j-1].type == CellType.Empty:
                            self.__cells[i][j-1] = cellClass(i, j)
                            

    def __setup_road_connections(self):
        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.__cells[i][j]
                if cell.type == CellType.Road:

                    # For intersections only
                    if len(cell.orientation) > 1:
                        # Always check two roads ahead, because the nearest may also be an intersection
                        # If there is a road below and it is not pointing upwards:
                        if (i + 2) < self.rows:
                            child = self.__cells[i + 2][j]
                            if child.type == CellType.Road and (len(child.orientation) > 1 or Direction.Up not in child.direction):
                                cell.addChild(self.__cells[i + 1][j])

                        # If there is a road above and it is not pointing downwards:
                        if (i - 2) >= 0:
                            child = self.__cells[i - 2][j]
                            if child.type == CellType.Road and (len(child.orientation) > 1 or Direction.Down not in child.direction):
                                cell.addChild(self.__cells[i - 1][j])

                        # If there is a road right and it is not pointing left:
                        if (j + 2) < self.cols:
                            child = self.__cells[i][j + 2]
                            if child.type == CellType.Road and (len(child.orientation) > 1 or Direction.Left not in child.direction):
                                cell.addChild(self.__cells[i][j + 1])

                        # If there is a road left and it is not pointing right:
                        if (j - 2) >= 0:
                            child = self.__cells[i][j - 2]
                            if child.type == CellType.Road and (len(child.orientation) > 1 or Direction.Right not in child.direction):
                                cell.addChild(self.__cells[i][j - 1])

                    if Direction.Up    in cell.direction and (i - 1) >= 0:        cell.addChild(self.__cells[i - 1][j])
                    if Direction.Down  in cell.direction and (i + 1) < self.rows: cell.addChild(self.__cells[i + 1][j])
                    if Direction.Left  in cell.direction and (j - 1) >= 0:        cell.addChild(self.__cells[i][j - 1])
                    if Direction.Right in cell.direction and (j + 1) < self.cols: cell.addChild(self.__cells[i][j + 1])

    def __setup_directions(self):
        # Horizontal pass
        for i in range(self.rows):
            j = 0
            while j < (self.cols - 1):
                curr_cell = self.__cells[i][j]
                next_cell = self.__cells[i][j + 1]

                if curr_cell.type == CellType.Road and Orientation.Vertical in curr_cell.orientation:
                    curr_cell.direction = [Direction.Down]
                    next_cell.direction = [Direction.Up]
                    j += 1

                j += 1

        # Vertical pass
        for j in range(self.cols):
            i = 0
            while i < (self.rows - 1):
                curr_cell = self.__cells[i][j]
                next_cell = self.__cells[i + 1][j]

                if curr_cell.type == CellType.Road and Orientation.Horizontal in curr_cell.orientation:
                    curr_cell.direction = [Direction.Left]
                    next_cell.direction = [Direction.Right]
                    i += 1

                i += 1

        # Intersections
        for intersection in self.intersections:
            cell = self.__cells[intersection[0]][intersection[1]]
            cell.orientation = [Orientation.Vertical, Orientation.Horizontal]

        for intersection in self.intersections:
            x = intersection[0]
            y = intersection[1]
            cell = self.__cells[x][y]
            neighbours = self.__get_road_neighbours(x, y)
            singles = self.__get_single_orientation(neighbours)
            cell.direction = [single.direction[0] for single in singles]


    def __get_single_orientation(self, cells):
        single_orientation = []
        for cell in cells:
            if len(cell.orientation) == 1:
                single_orientation.append(cell)
        return single_orientation


    def __get_road_neighbours(self, x, y):
        neighbours = []
        for i in range(-1, +2):
            for j in range(-1, +2):
                xx = x + i
                yy = y + j
                if (i == 0 or j == 0) and not (i == 0 and j == 0) and xx > 0 and yy > 0 and xx < self.rows and yy < self.cols:
                    cell = self.__cells[xx][yy]
                    if cell.type == CellType.Road:
                        neighbours.append(cell)
        return neighbours


    def __duplicate_elements(self, elements):
        new_elements = []
        for el in elements:
            new_elements.append(el)
            new_elements.append(el.duplicate())
        return new_elements

    def __subdivide_grid(self):

        # Duplicate cells
        updated_cells = []
        for i, row in enumerate(self.__cells):
            new_row = [cell.duplicate() if cell.type == CellType.Road else CellEmpty() for cell in row]
            updated_cells.append(self.__duplicate_elements(row))
            updated_cells.append(self.__duplicate_elements(new_row))
        self.__cells = updated_cells

        # Fix row and col numbers
        for row in range(self.rows):
            for col in range(self.cols):
                self.__cells[row][col].row = row
                self.__cells[row][col].col = col

        new_intersections = []
        for intersection in self.intersections:
            x = intersection[0] * 2
            y = intersection[1] * 2
            new_intersections.append((x, y))
            new_intersections.append((x + 1, y))
            new_intersections.append((x, y + 1))
            new_intersections.append((x + 1, y + 1))

        self.intersections = new_intersections


    def __is_border(self, corner, rows, cols):
        if corner[0] in [0, rows - 1]: return True
        if corner[1] in [0, cols - 1]: return True
        return False

    def __build_road(self, corners, orientation):
        x1 = corners[0][1] # Col 1
        x2 = corners[1][1] # Col 2
        y1 = corners[0][0] # Row 1
        y2 = corners[1][0] # Row 2

        if abs(y1 - y2) > 0:
            start = min([y1, y2])
            final = max([y1, y2]) + 1
            for y in range(start, final):
                self.__cells[y][x1] = CellRoad(y, x1)
                self.__cells[y][x1].orientation = [orientation]
        else:
            start = min([x1, x2])
            final = max([x1, x2]) + 1
            for x in range(start, final):
                self.__cells[y1][x] = CellRoad(y1, x)
                self.__cells[y1][x].orientation = [orientation]

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
