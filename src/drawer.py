import pygame
from time import time, sleep
from math import floor
from cell import CellType

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
            color = (80, 80, 80) if map.grid.get(row, col).type == CellType.Road else (255, 255, 255)
            pygame.draw.rect(screen, color, (x, y, size_x, size_y), 0)
