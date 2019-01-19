from grid import Grid
from car import Car

from cell import Lights, CellType
import random as rnd

class City:
    MAX_CARS = 20
    MAX_SPAWN_PER_STEP = 3

    def __init__(self, rows, cols, n_intersections):
        self.grid = Grid(rows, cols, n_intersections)
        self.cars = []
        self.cars_despawned = 0
        self.cars_spawned = 0
        self.onNewCar = None
        self.onDelCar = None

    def get(self, row, col):
        return self.grid.get(row, col)

    def step(self):
        self.__despawn_cars()
        self.__move_cars()

        i = 0
        while len(self.cars) < City.MAX_CARS and i < City.MAX_SPAWN_PER_STEP:
            self.__spawn_car()
            i += 1

        for i in range(self.grid.cols):
            for j in range(self.grid.rows):
                cell = self.grid.get(j, i)
                if cell.type == CellType.Road and cell.hasLights and rnd.random() < 0.1:
                    cell.lights = Lights.CARS_GREEN if cell.lights == Lights.CARS_RED else Lights.CARS_RED

    def __despawn_cars(self):
        new_cars = self.cars.copy()
        for car in self.cars:
            if car.cell == car.despawn:
                car.cell.car = None
                new_cars.remove(car)
                self.cars_despawned += 1

                if self.onDelCar is not None:
                    self.onDelCar(car)

        self.cars = new_cars

    def __spawn_car(self):
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
        self.cars_spawned += 1

        if self.onNewCar is not None:
            self.onNewCar(car)


    def __move_cars(self):
        for car in self.cars:
            car.move()
