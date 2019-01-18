from grid import Grid


class City:

    def __init__(self, rows, cols, n_intersections):
        self.grid = Grid(rows, cols, n_intersections)

    def get(self, row, col):
        return self.grid.get(row, col)
