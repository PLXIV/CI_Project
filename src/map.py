from grid import Grid

class Map:

    def __init__(self, rows, cols, n_intersections):
        self.grid = Grid(rows, cols, n_intersections)

    def get(self, row, col):
        return self.grid.get(row, col)

if __name__ == "__main__":
    map = Map(rows=20, cols=10, n_intersections=10)
    map.grid.generate()
    print(map.grid)
    print(map.grid.intersections)