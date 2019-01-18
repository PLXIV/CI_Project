import random as rnd


class Car:

    def __init__(self, spawns, despawns):
        self.spawn = rnd.choice(spawns)
        self.despawn = rnd.choice(despawns)
        self.cell = self.spawn
        self.cell.car = self

    def move(self):
        self.cell.car = None
        self.cell = rnd.choice(self.cell.children)
        self.cell.car = self
