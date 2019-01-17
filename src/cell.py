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

    def __init__(self, cell_type):
        self.type = cell_type

    def __str__(self):
        if self.type == CellType.Road:
            return "■"
        else:
            return "□"


class CellRoad(Cell):

    def __init__(self):
        super().__init__(CellType.Road)
        self.direction = RoadDir.Unknown
        self.orientation = Orientation.Unknown
        self.next = None

    def duplicate(self):
        dupli = CellRoad()
        dupli.direction = self.direction
        dupli.orientation = self.orientation
        dupli.next = self.next
        return dupli

class CellBuilding(Cell):

    def __init__(self):
        super().__init__(CellType.Building)


class CellSidewalk(Cell):

    def __init__(self):
        super().__init__(CellType.Sidewalk)


class CellEmpty(Cell):

    def __init__(self):
        super().__init__(CellType.Empty)

    def duplicate(self):
        return CellEmpty()