from enum import Enum


class CellType(Enum):
    Road = 1
    Building = 2
    Sidewalk = 3
    Empty = 4


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


class CellBuilding(Cell):

    def __init__(self):
        super().__init__(CellType.Building)


class CellSidewalk(Cell):

    def __init__(self):
        super().__init__(CellType.Sidewalk)


class CellEmpty(Cell):

    def __init__(self):
        super().__init__(CellType.Empty)