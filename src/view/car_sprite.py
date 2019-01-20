import pygame


class CarSprite(pygame.sprite.Sprite):

    def __init__(self, image, size, car, margin_w, margin_h):
        pygame.sprite.Sprite.__init__(self)
        self.original = image
        self.car = car
        self.margin_w = margin_w
        self.margin_h = margin_h
        self.size = size
        self.degrees = 0

        if image is None:
            self.image = pygame.Surface([size, size])
            self.image.fill((0, 0, 0))
        else:
            self.image = pygame.transform.scale(self.original, (size, size))
            self.image.set_colorkey((0, 0, 0))

        self.rotate()
        self.rect = self.image.get_rect()
        self.rect.x = margin_w + car.cell.col * size
        self.rect.y = margin_h + car.cell.row * size

    def rotate(self):
        target_degrees = 0
        next_cell = self.car.getNextCell()

        if next_cell is None:
            return

        if next_cell.col == self.car.cell.col + 1:
            target_degrees = 0
        if next_cell.row == self.car.cell.row + 1:
            target_degrees = 270
        elif next_cell.row == self.car.cell.row - 1:
            target_degrees = 90
        elif next_cell.col == self.car.cell.col - 1:
            target_degrees = 180

        self.image = pygame.transform.rotate(self.image,  target_degrees - self.degrees)
        self.degrees = target_degrees

    def resize(self, size, margin_w, margin_h):
        self.margin_w = margin_w
        self.margin_h = margin_h
        self.size = size
        if self.original is None:
            self.image = pygame.Surface([size, size])
            self.image.fill((0, 0, 0))
        else:
            self.image = pygame.transform.scale(self.original, (size, size))
            self.image.set_colorkey((0, 0, 0))
        self.degrees = 0
        self.rotate()
        self.rect = self.image.get_rect()
        self.rect.x = margin_w + self.car.cell.col * size
        self.rect.y = margin_h + self.car.cell.row * size

    def update(self):
        self.rotate()
        self.rect.x = self.margin_w + self.car.cell.col * self.size
        self.rect.y = self.margin_h + self.car.cell.row * self.size