import pygame
from time import time, sleep
from math import floor
from cell import CellType, RoadDir
from square import Orientation

WIDTH = 600
HEIGHT = 600
MARGIN = 10

def display(map):
    pygame.init()
    pygame.display.set_caption("CI project")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    running = True

    fps = 30
    now = time()
    next_frame = now + 1.0 / fps
    while running:
        # Step
        step(screen, map)
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # Update
        pygame.display.update()
        # Frames
        while now < next_frame:
            sleep(next_frame - now)
            now = time()
        next_frame += 1.0 / fps

def step(screen, map):
    screen.fill((255, 255, 255))

    size_x = floor((WIDTH - MARGIN * 2) / map.grid.cols)
    size_y = floor((HEIGHT - MARGIN * 2) / map.grid.rows)

    for row in range(0, map.grid.rows):
        for col in range(0, map.grid.cols):
            x = MARGIN + col * size_x
            y = MARGIN + row * size_y
            color = (0, 0, 0)
            cell = map.grid.get(row, col)
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
            pygame.draw.rect(screen, color, (x, y, size_x, size_y), 0)
