import pygame
from pygame.time import Clock
from math import ceil
from cell import CellType, RoadDir
from view.fps_counter import FPSCounter
from view.cell_sprite import CellSprite
import view.locations as loc

class Drawer:

    def __init__(self, fps_target, city, width, height, margin=0):
        pygame.init()
        pygame.display.set_caption("CI project")

        self.clock = Clock()
        self.w = width
        self.h = height
        self.margin = margin
        self.city = city
        self.fps_target = fps_target
        self.fps_counter = FPSCounter()
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.running = False
        self.cell_group = None

        self.__gen_road_groups()

    def __gen_road_groups(self):
        self.cell_group = pygame.sprite.Group()

        size_x = ceil((self.w - self.margin * 2) / self.city.grid.cols)
        size_y = ceil((self.h - self.margin * 2) / self.city.grid.rows)

        images = {
            loc.ROAD_UP:      pygame.image.load(loc.ROAD_UP).convert(),
            loc.ROAD_DOWN:    pygame.image.load(loc.ROAD_DOWN).convert(),
            loc.ROAD_LEFT:    pygame.image.load(loc.ROAD_LEFT).convert(),
            loc.ROAD_RIGHT:   pygame.image.load(loc.ROAD_RIGHT).convert(),
            loc.ROAD_CROSS:   pygame.image.load(loc.ROAD_CROSS).convert(),
            loc.SIDEWALK:     pygame.image.load(loc.SIDEWALK).convert(),
            loc.HOUSE:        pygame.image.load(loc.HOUSE).convert(),
            loc.ROAD_T_DOWN:  pygame.image.load(loc.ROAD_T_DOWN).convert(),
            loc.ROAD_T_UP:    pygame.image.load(loc.ROAD_T_UP).convert(),
            loc.ROAD_T_LEFT:  pygame.image.load(loc.ROAD_T_LEFT).convert(),
            loc.ROAD_T_RIGHT: pygame.image.load(loc.ROAD_T_RIGHT).convert(),
        }

        for row in range(0, self.city.grid.rows):
            for col in range(0, self.city.grid.cols):
                x = self.margin + col * size_x
                y = self.margin + row * size_y

                cell = self.city.grid.get(row, col)
                
                if cell.type == CellType.Sidewalk:
                    image = images[loc.SIDEWALK]
                    self.cell_group.add(CellSprite(image, size_x, size_y, x, y))

                if cell.type == CellType.Building:
                    image = images[loc.HOUSE]
                    self.cell_group.add(CellSprite(image, size_x, size_y, x, y))

                if cell.type == CellType.Road:
                    image = None
                    active_sides = cell.active_sides()

                    if len(active_sides) == 4:
                        image = images[loc.ROAD_CROSS]

                    elif len(active_sides) == 3:
                        if   RoadDir.Up    not in active_sides: image = images[loc.ROAD_T_UP]
                        elif RoadDir.Down  not in active_sides: image = images[loc.ROAD_T_DOWN]
                        elif RoadDir.Left  not in active_sides: image = images[loc.ROAD_T_LEFT]
                        elif RoadDir.Right not in active_sides: image = images[loc.ROAD_T_RIGHT]

                    elif cell.hasCrosswalk:
                        pass
                        #if   RoadDir.Up    in cell.direction: image = images[loc.ROAD_DOWN]
                        #elif RoadDir.Down  in cell.direction: image = images[loc.ROAD_UP]
                        #elif RoadDir.Left  in cell.direction: image = images[loc.ROAD_RIGHT]
                    #elif RoadDir.Right in cell.direction: image = images[loc.ROAD_LEFT]

                    else:
                        if   RoadDir.Up    in cell.direction: image = images[loc.ROAD_UP]
                        elif RoadDir.Down  in cell.direction: image = images[loc.ROAD_DOWN]
                        elif RoadDir.Left  in cell.direction: image = images[loc.ROAD_LEFT]
                        elif RoadDir.Right in cell.direction: image = images[loc.ROAD_RIGHT]

                    self.cell_group.add(CellSprite(image, size_x, size_y, x, y))

    def run(self):
        self.running = True

        while self.running:
            self.__step()
            self.__events()
            pygame.display.update()
            # Frames
            print('\rFPS: {:.1f}  '.format(self.fps_counter.tick()) + " " + str(self.running), end='')
            self.clock.tick(self.fps_target)

    def __events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def __step(self):
        self.screen.fill((255, 255, 255))
        self.cell_group.draw(self.screen)
