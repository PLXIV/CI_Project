from enum import Enum


class Orientation(Enum):
    Horizontal = 1
    Vertical = 2
    Unknown = 3


class CellType(Enum):
    Road = 1
    Building = 2
    Sidewalk = 3
    Empty = 4


class RoadDir(Enum):
    Up = 1
    Down = 2
    Left = 3
    Right = 4
    Unknown = 5


class Cell:

    def __init__(self, cell_type, row, col):
        self.type = cell_type
        self.row = row
        self.col = col

    def __str__(self):
        if self.type == CellType.Road:
            return "■"
        else:
            return "□"

    def __repr__(self):
        return '({:d},{:d})'.format(self.row, self.col)

class CellRoad(Cell):

    def __init__(self, row, col):
        super().__init__(CellType.Road, row, col)
        self.direction = [RoadDir.Unknown]
        self.orientation = [Orientation.Unknown]
        self.children = []
        self.parents = []

    def addChild(self, child):
        if child not in self.children:
            self.children.append(child)
            child.parents.append(self)

    def duplicate(self):
        dupli = CellRoad(self.row, self.col)
        dupli.direction = self.direction.copy()
        dupli.orientation = self.orientation.copy()
        dupli.children = self.children.copy()
        dupli.parents = self.parents.copy()
        return dupli

    def active_sides(self):
        active = []
        for element_list in [self.children, self.parents]:
            for element in element_list:
                if element.row == self.row + 1:
                    active.append(RoadDir.Down)
                elif element.row == self.row - 1:
                    active.append(RoadDir.Up)
                elif element.col == self.col + 1:
                    active.append(RoadDir.Right)
                elif element.col == self.col - 1:
                    active.append(RoadDir.Left)
        return active

class CellBuilding(Cell):

    def __init__(self, row, col):
        super().__init__(CellType.Building, row, col)


class CellSidewalk(Cell):

    def __init__(self, row, col):
        super().__init__(CellType.Sidewalk, row, col)


class CellEmpty(Cell):

    def __init__(self, row=0, col=0):
        super().__init__(CellType.Empty, row, col)

    def duplicate(self):
        return CellEmpty(self.row, self.col)