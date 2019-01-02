from enum import Enum


class CellType(Enum):
    Road = 1
    Building = 2


class Cell:

    def __init__(self, cell_type):
        self.type = cell_type

    def __str__(self):
        if self.type == CellType.Road:
            return "■"
        if self.type == CellType.Building:
            return "□"
