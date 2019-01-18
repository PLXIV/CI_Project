import pygame
from time import time, sleep
from math import ceil
from cell import CellType, RoadDir
from view.fps_counter import FPSCounter


class Drawer:

    def __init__(self, fps_target, city, width, height, margin=0):
        pygame.init()
        pygame.display.set_caption("CI project")

        self.w = width
        self.h = height
        self.margin = margin
        self.city = city
        self.fps_target = fps_target
        self.fps_counter = FPSCounter()
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.running = False

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def run(self):
        self.running = True

        now = time()
        next_frame = now + 1.0 / self.fps_target
        while self.running:
            self.step()
            self.events()
            pygame.display.update()
            # Frames
            print('\rFPS: {:.1f}  '.format(self.fps_counter.tick()), end='')
            while now < next_frame:
                sleep(next_frame - now)
                now = time()
            next_frame += 1.0 / self.fps_target

    def step(self):
        self.screen.fill((255, 255, 255))

        size_x = ceil((self.w - self.margin * 2) / self.city.grid.cols)
        size_y = ceil((self.h - self.margin * 2) / self.city.grid.rows)

        for row in range(0, self.city.grid.rows):
            for col in range(0, self.city.grid.cols):
                x = self.margin + col * size_x
                y = self.margin + row * size_y
                color = (0, 0, 0)
                cell = self.city.grid.get(row, col)
                if cell.type == CellType.Road:
                    if RoadDir.Up in cell.direction and RoadDir.Left in cell.direction:
                        color = (255, 0, 255)
                    elif RoadDir.Up in cell.direction and RoadDir.Right in cell.direction:
                        color = (0, 0, 255)
                    elif RoadDir.Down in cell.direction and RoadDir.Left in cell.direction:
                        color = (0, 255, 0)
                    elif RoadDir.Down in cell.direction and RoadDir.Right in cell.direction:
                        color = (255, 0, 0)
                    elif RoadDir.Up in cell.direction:
                        color = (150, 150, 150)
                    elif RoadDir.Down in cell.direction:
                        color = (200, 200, 200)
                    elif RoadDir.Left in cell.direction:
                        color = (100, 100, 100)
                    elif RoadDir.Right in cell.direction:
                        color = (0, 0, 0)
                    elif RoadDir.Unknown in cell.direction:
                        color = (80, 80, 80)
                else:
                    color = (255, 255, 255)
                pygame.draw.rect(self.screen, color, (x, y, size_x, size_y), 0)
