import pygame
from pygame.time import Clock
from math import ceil, floor
from cell import CellType, Direction
from view.fps_counter import FPSCounter
from view.cell_sprite import CellSprite
import view.locations as loc
from random import choice


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
        self.screen = pygame.display.set_mode((self.w, self.h),  pygame.RESIZABLE)
        self.running = False
        self.cell_group = None

        self.__gen_road_sprites()

    def __sprite_size(self):
        return ceil((min(self.w, self.h) - self.margin * 2) / self.city.grid.cols)

    def __resize_sprites(self):
        size = self.__sprite_size()
        margin_w = floor((self.w - size * self.city.grid.cols) / 2)
        margin_h = floor((self.h - size * self.city.grid.rows) / 2)

        for sprite in self.cell_group:
            x = margin_w + self.margin + sprite.col * size
            y = margin_h + self.margin + sprite.row * size
            sprite.resize(size, x, y)

    def __gen_road_sprites(self):
        self.cell_group = pygame.sprite.Group()
        size = self.__sprite_size()
        margin_w = floor((self.w - size * self.city.grid.cols) / 2)
        margin_h = floor((self.h - size * self.city.grid.rows) / 2)

        images = {
            loc.ROAD_UP:      pygame.image.load(loc.ROAD_UP).convert(),
            loc.ROAD_DOWN:    pygame.image.load(loc.ROAD_DOWN).convert(),
            loc.ROAD_LEFT:    pygame.image.load(loc.ROAD_LEFT).convert(),
            loc.ROAD_RIGHT:   pygame.image.load(loc.ROAD_RIGHT).convert(),
            loc.ROAD_CROSS:   pygame.image.load(loc.ROAD_CROSS).convert(),
            loc.SIDEWALK:     pygame.image.load(loc.SIDEWALK).convert(),
            loc.HOUSE_1:      pygame.image.load(loc.HOUSE_1).convert(),
            loc.HOUSE_2:      pygame.image.load(loc.HOUSE_2).convert(),
            loc.HOUSE_3:      pygame.image.load(loc.HOUSE_3).convert(),
            loc.HOUSE_4:      pygame.image.load(loc.HOUSE_4).convert(),
            loc.HOUSE_5:      pygame.image.load(loc.HOUSE_5).convert(),
            loc.HOUSE_6:      pygame.image.load(loc.HOUSE_6).convert(),
            loc.ROAD_T_DOWN:  pygame.image.load(loc.ROAD_T_DOWN).convert(),
            loc.ROAD_T_UP:    pygame.image.load(loc.ROAD_T_UP).convert(),
            loc.ROAD_T_LEFT:  pygame.image.load(loc.ROAD_T_LEFT).convert(),
            loc.ROAD_T_RIGHT: pygame.image.load(loc.ROAD_T_RIGHT).convert(),
            loc.ROAD_CROSSWALK_H: pygame.image.load(loc.ROAD_CROSSWALK_H).convert(),
            loc.ROAD_CROSSWALK_V: pygame.image.load(loc.ROAD_CROSSWALK_V).convert(),
        }

        for row in range(0, self.city.grid.rows):
            for col in range(0, self.city.grid.cols):
                x = margin_h + self.margin + col * size
                y = margin_w + self.margin + row * size
                cell = self.city.grid.get(row, col)
                image = None
                
                if cell.type == CellType.Sidewalk:
                    image = images[loc.SIDEWALK]

                if cell.type == CellType.Building:
                    house_array = [loc.HOUSE_1, loc.HOUSE_3, loc.HOUSE_4, loc.HOUSE_5, loc.HOUSE_6]
                    image = images[choice(house_array)]

                if cell.type == CellType.Road:
                    active_sides = cell.active_sides()

                    if len(active_sides) == 4:
                        image = images[loc.ROAD_CROSS]

                    elif len(active_sides) == 3:
                        if   Direction.Up    not in active_sides: image = images[loc.ROAD_T_UP]
                        elif Direction.Down  not in active_sides: image = images[loc.ROAD_T_DOWN]
                        elif Direction.Left  not in active_sides: image = images[loc.ROAD_T_LEFT]
                        elif Direction.Right not in active_sides: image = images[loc.ROAD_T_RIGHT]

                    elif cell.hasCrosswalk:
                        if   Direction.Up    in cell.direction: image = images[loc.ROAD_CROSSWALK_V]
                        elif Direction.Down  in cell.direction: image = images[loc.ROAD_CROSSWALK_V]
                        elif Direction.Left  in cell.direction: image = images[loc.ROAD_CROSSWALK_H]
                        elif Direction.Right in cell.direction: image = images[loc.ROAD_CROSSWALK_H]

                    else:
                        if   Direction.Up    in cell.direction: image = images[loc.ROAD_UP]
                        elif Direction.Down  in cell.direction: image = images[loc.ROAD_DOWN]
                        elif Direction.Left  in cell.direction: image = images[loc.ROAD_LEFT]
                        elif Direction.Right in cell.direction: image = images[loc.ROAD_RIGHT]

                if cell.type != CellType.Empty:
                    self.cell_group.add(CellSprite(image, size, x, y, row, col))

    def run(self):
        self.running = True

        while self.running:
            self.__step()
            self.__events()
            pygame.display.update()
            print('\rFPS: {:.1f}  '.format(self.fps_counter.tick()), end='')
            self.clock.tick(self.fps_target)

        pygame.quit()

    def __events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.VIDEORESIZE:
                self.w = event.w
                self.h = event.h
                self.screen = pygame.display.set_mode((self.w, self.h), pygame.RESIZABLE)
                self.__resize_sprites()

    def __step(self):
        self.screen.fill((255, 255, 255))
        self.cell_group.draw(self.screen)
