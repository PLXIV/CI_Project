from grid import Grid
from car import Car

class City:

    def __init__(self, rows, cols, n_intersections):
        self.grid = Grid(rows, cols, n_intersections)
        self.cars = []
        self.onNewCar = None
        self.onDelCar = None

    def get(self, row, col):
        return self.grid.get(row, col)

    def step(self):
        self.__move_cars()
        if len(self.cars) < 5:
            self.__spawn_cars()

    def __spawn_cars(self):
        spawns = self.grid.spawn_roads
        despawns = self.grid.despawn_roads
        free_spawns = []

        for spawn in spawns:
            if spawn.car is None:
                free_spawns.append(spawn)

        if len(free_spawns) == 0:
            print('No free spawn points!')
            return

        car = Car(free_spawns, despawns)
        self.cars.append(car)

        if self.onNewCar is not None:
            self.onNewCar(car)


    def __move_cars(self):
        for car in self.cars:
            car.move()
