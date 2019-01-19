import random as rnd
from cell import Lights

class Car:

    def __init__(self, spawns, despawns):
        self.spawn = rnd.choice(spawns)
        self.despawn = rnd.choice(despawns)
        self.cell = self.spawn
        self.cell.car = self

    def getNextCell(self):
        return self.cell.destinations[self.despawn]

    def move(self):
        next_cell = self.getNextCell()

        if next_cell.car is None and (not next_cell.hasLights or next_cell.lights == Lights.CARS_GREEN):
            self.cell.car = None
            self.cell = next_cell
            self.cell.car = self

