import pygame
from pygame.time import Clock
from math import ceil, floor
from city.cell import CellType, Direction
from view.fps_counter import FPSCounter
from view.cell_sprite import CellSprite
from view.car_sprite import CarSprite
from view.light_cell_sprite import LightsCellSprite
import view.locations as loc
from random import choice


class Drawer:

    def __init__(self, fps_target, city, width, height, options):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("CI project")

        self.options = options
        self.font = pygame.font.SysFont('arial', 16)
        self.clock = Clock()
        self.w = width
        self.h = height
        self.city = city
        self.fps_target = fps_target
        self.fps_counter = FPSCounter()
        self.screen = pygame.display.set_mode((self.w, self.h),  pygame.RESIZABLE)
        self.running = False
        self.cell_group = None
        self.cars_group = None
        self.images = {}
        self.__load_images()
        self.__gen_sprites()
        self.city.onNewCar = self.__addCar
        self.city.onDelCar = self.__delCar

    def __load_images(self):
        self.images = {
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
            loc.CAR_1:        pygame.image.load(loc.CAR_1).convert(),
            loc.CAR_2:        pygame.image.load(loc.CAR_2).convert(),
            loc.CAR_3:        pygame.image.load(loc.CAR_3).convert(),

            loc.ROAD_CROSSWALK_H:           pygame.image.load(loc.ROAD_CROSSWALK_H).convert(),
            loc.ROAD_CROSSWALK_V:           pygame.image.load(loc.ROAD_CROSSWALK_V).convert(),
            loc.ROAD_CROSSWALK_LEFT_RED:    pygame.image.load(loc.ROAD_CROSSWALK_LEFT_RED).convert(),
            loc.ROAD_CROSSWALK_RIGHT_RED:   pygame.image.load(loc.ROAD_CROSSWALK_RIGHT_RED).convert(),
            loc.ROAD_CROSSWALK_TOP_RED:     pygame.image.load(loc.ROAD_CROSSWALK_TOP_RED).convert(),
            loc.ROAD_CROSSWALK_BOT_RED:     pygame.image.load(loc.ROAD_CROSSWALK_BOT_RED).convert(),
            loc.ROAD_CROSSWALK_LEFT_GREEN:  pygame.image.load(loc.ROAD_CROSSWALK_LEFT_GREEN).convert(),
            loc.ROAD_CROSSWALK_RIGHT_GREEN: pygame.image.load(loc.ROAD_CROSSWALK_RIGHT_GREEN).convert(),
            loc.ROAD_CROSSWALK_TOP_GREEN:   pygame.image.load(loc.ROAD_CROSSWALK_TOP_GREEN).convert(),
            loc.ROAD_CROSSWALK_BOT_GREEN:   pygame.image.load(loc.ROAD_CROSSWALK_BOT_GREEN).convert(),
        }

    def __addCar(self, car):
        size, margin_w, margin_h = self.__sprite_size()
        car_image = choice([loc.CAR_1, loc.CAR_2, loc.CAR_3])
        self.cars_group.add(CarSprite(self.images[car_image], size, car, margin_w, margin_h))

    def __delCar(self, car):
        for car_sprite in self.cars_group:
            if car_sprite.car == car:
                self.cars_group.remove(car_sprite)
                return

    def __sprite_size(self):
        size = ceil((min(self.w, self.h)) / self.city.grid.cols)
        margin_w = floor((self.w - size * self.city.grid.cols) / 2)
        margin_h = floor((self.h - size * self.city.grid.rows) / 2)
        return size, margin_w, margin_h

    def __resize_sprites(self):
        size, margin_w, margin_h = self.__sprite_size()

        for sprite in self.cell_group:
            sprite.resize(size, margin_w, margin_h)

        for sprite in self.cars_group:
            sprite.resize(size, margin_w, margin_h)

    def __gen_sprites(self):
        self.cell_group = pygame.sprite.Group()
        self.cars_group = pygame.sprite.Group()
        size, margin_w, margin_h = self.__sprite_size()

        for row in range(0, self.city.grid.rows):
            for col in range(0, self.city.grid.cols):
                cell = self.city.grid.get(row, col)
                image = None
                
                if cell.type == CellType.Sidewalk:
                    image = self.images[loc.SIDEWALK]
                    self.cell_group.add(CellSprite(image, size, cell, margin_w, margin_h))

                if cell.type == CellType.Building:
                    house_array = [loc.HOUSE_1, loc.HOUSE_3, loc.HOUSE_4, loc.HOUSE_5, loc.HOUSE_6]
                    image = self.images[choice(house_array)]
                    self.cell_group.add(CellSprite(image, size, cell, margin_w, margin_h))

                if cell.type == CellType.Road:
                    active_sides = cell.active_sides()

                    if len(active_sides) == 4:
                        image = self.images[loc.ROAD_CROSS]
                        self.cell_group.add(CellSprite(image, size, cell, margin_w, margin_h))

                    elif len(active_sides) == 3:
                        if   Direction.Up    not in active_sides: image = self.images[loc.ROAD_T_UP]
                        elif Direction.Down  not in active_sides: image = self.images[loc.ROAD_T_DOWN]
                        elif Direction.Left  not in active_sides: image = self.images[loc.ROAD_T_LEFT]
                        elif Direction.Right not in active_sides: image = self.images[loc.ROAD_T_RIGHT]
                        self.cell_group.add(CellSprite(image, size, cell, margin_w, margin_h))

                    elif cell.hasCrosswalk and cell.hasLights:
                        image = []
                        if Direction.Up in cell.direction:
                            image.append(self.images[loc.ROAD_CROSSWALK_BOT_RED] if cell.neighbours_intersections()[Direction.Up] is not None else self.images[loc.ROAD_CROSSWALK_TOP_RED])
                            image.append(self.images[loc.ROAD_CROSSWALK_BOT_GREEN] if cell.neighbours_intersections()[Direction.Up] is not None else self.images[loc.ROAD_CROSSWALK_TOP_GREEN])
                        elif Direction.Down in cell.direction:
                            image.append(self.images[loc.ROAD_CROSSWALK_BOT_RED] if cell.neighbours_intersections()[Direction.Up] is not None else self.images[loc.ROAD_CROSSWALK_TOP_RED])
                            image.append(self.images[loc.ROAD_CROSSWALK_BOT_GREEN] if cell.neighbours_intersections()[Direction.Up] is not None else self.images[loc.ROAD_CROSSWALK_TOP_GREEN])
                        elif Direction.Left in cell.direction:
                            image.append(self.images[loc.ROAD_CROSSWALK_LEFT_RED] if cell.neighbours_intersections()[Direction.Left] is not None else self.images[loc.ROAD_CROSSWALK_RIGHT_RED])
                            image.append(self.images[loc.ROAD_CROSSWALK_LEFT_GREEN] if cell.neighbours_intersections()[Direction.Left] is not None else self.images[loc.ROAD_CROSSWALK_RIGHT_GREEN])
                        elif Direction.Right in cell.direction:
                            image.append(self.images[loc.ROAD_CROSSWALK_LEFT_RED] if cell.neighbours_intersections()[Direction.Left] is not None else self.images[loc.ROAD_CROSSWALK_RIGHT_RED])
                            image.append(self.images[loc.ROAD_CROSSWALK_LEFT_GREEN] if cell.neighbours_intersections()[Direction.Left] is not None else self.images[loc.ROAD_CROSSWALK_RIGHT_GREEN])
                        self.cell_group.add(LightsCellSprite(image, size, cell, margin_w, margin_h))

                    elif cell.hasCrosswalk:
                        if   Direction.Up    in cell.direction: image = self.images[loc.ROAD_CROSSWALK_V]
                        elif Direction.Down  in cell.direction: image = self.images[loc.ROAD_CROSSWALK_V]
                        elif Direction.Left  in cell.direction: image = self.images[loc.ROAD_CROSSWALK_H]
                        elif Direction.Right in cell.direction: image = self.images[loc.ROAD_CROSSWALK_H]
                        self.cell_group.add(CellSprite(image, size, cell, margin_w, margin_h))

                    else:
                        if   Direction.Up    in cell.direction: image = self.images[loc.ROAD_UP]
                        elif Direction.Down  in cell.direction: image = self.images[loc.ROAD_DOWN]
                        elif Direction.Left  in cell.direction: image = self.images[loc.ROAD_LEFT]
                        elif Direction.Right in cell.direction: image = self.images[loc.ROAD_RIGHT]
                        self.cell_group.add(CellSprite(image, size, cell, margin_w, margin_h))

    def run(self):
        self.running = True

        while self.running:
            self.__step()
            self.__events()
            pygame.display.update()
            self.clock.tick(self.fps_target)

        pygame.quit()
        self.options[0] = True

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
        self.cars_group.draw(self.screen)
        self.cell_group.update()
        self.cars_group.update()

        fps_str = 'FPS: {:.1f}  '.format(self.fps_counter.tick())
        fps_tex = self.font.render(fps_str, False, (0, 0, 0))
        self.screen.blit(fps_tex,(5,5))


