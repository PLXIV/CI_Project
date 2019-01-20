import random as rnd
from city.cell import Lights

class Car:

    def __init__(self, spawns, despawns):
        despawns = list(despawns)
        self.spawn = rnd.choice(spawns)
        self.despawn = None

        # Prevent spawn and despawns that are unreachable
        while self.despawn is None and len(despawns) > 0:
            self.despawn = rnd.choice(despawns)
            if self.spawn.destinations[self.despawn] is None:
                despawns.remove(self.despawn)
                self.despawn = None

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

