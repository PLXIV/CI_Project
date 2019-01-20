from city.grid import Grid
from city.car import Car
from city.cell import Lights

from copy import deepcopy
from math import ceil
from time import sleep
import numpy as np

class City:
    MAX_CARS = 100
    MAX_SPAWN_PER_STEP = 8

    def __init__(self, rows, cols, n_intersections):
        self.grid = Grid(rows, cols, n_intersections)
        self.cars = []
        self.cars_despawned = 0
        self.cars_spawned = 0
        self.onNewCar = None
        self.onDelCar = None

    @staticmethod
    def generate(rows, cols, n_intersections, seed=None):
        city = City(rows, cols, n_intersections)
        if seed is not None:
            city.grid.generate(seed)
        else:
            city.grid.generate()
        return city

    def clone(self):
        cloned = City(self.grid.rows, self.grid.cols, self.grid.n_intersections)
        cloned.grid = deepcopy(self.grid)
        return cloned

    def clean(self):
        self.cars_despawned = 0
        self.cars_spawned = 0
        for car in self.cars:
            car.cell.car = None
            if self.onDelCar is not None:
                self.onDelCar(car)
        self.cars = []

    def get(self, row, col):
        return self.grid.get(row, col)

    def step(self, light_values = None):
        self.__despawn_cars()
        self.__move_cars()
        self.__spawn_cars()
        if light_values is not None:
            self.__set_lights(light_values)

    def run(self, gene, sim_steps, light_duration_steps, sim_time=0.3, options=None):
        lights_steps = ceil(sim_steps / light_duration_steps) + 1
        lights_gene = np.reshape(gene, [len(self.grid.roads_with_lights), lights_steps]).T

        for i in range(sim_steps):
            lights = lights_gene[ceil(i / light_duration_steps), :]
            self.step(lights)

            if sim_time > 0:  # Wait time
                sleep(sim_time)

            if options is not None and options[0]:  # Quit option
                return

    def __set_lights(self, light_values):
        for i, cell in enumerate(self.grid.roads_with_lights):
            cell.lights = Lights.CARS_GREEN if light_values[i] else Lights.CARS_RED

    def __spawn_cars(self):
        i = 0
        while len(self.cars) < City.MAX_CARS and i < City.MAX_SPAWN_PER_STEP:
            self.__spawn_car()
            i += 1

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
            # print('No free spawn points!')
            return

        car = Car(free_spawns, despawns)
        self.cars.append(car)
        self.cars_spawned += 1

        if self.onNewCar is not None:
            self.onNewCar(car)

    def __move_cars(self):
        for car in self.cars:
            car.move()
