import pygame
from cell import Lights


class LightsCellSprite(pygame.sprite.Sprite):
    RED = 0
    GREEN = 1

    def __init__(self, images, size, cell, margin_w, margin_h):
        pygame.sprite.Sprite.__init__(self)
        self.originals = images
        self.cell = cell
        self.margin_w = margin_w
        self.margin_h = margin_h
        self.size = size

        if images is None:
            self.image = pygame.Surface([size, size])
            self.image.fill((0, 0, 0))
        else:
            state = LightsCellSprite.RED if (cell.lights == Lights.CARS_RED) else LightsCellSprite.GREEN
            self.image = pygame.transform.scale(self.originals[state], (size, size))
            self.image.set_colorkey((255, 255, 255))

        self.rect = self.image.get_rect()
        self.rect.x = margin_w + cell.col * size
        self.rect.y = margin_h + cell.row * size

    def resize(self, size, margin_w, margin_h):
        if self.originals is None:
            self.image = pygame.Surface([size, size])
            self.image.fill((0, 0, 0))
        else:
            state = LightsCellSprite.RED if (self.cell.lights == Lights.CARS_RED) else LightsCellSprite.GREEN
            self.image = pygame.transform.scale(self.originals[state], (size, size))
            self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = margin_w + self.cell.col * size
        self.rect.y = margin_h + self.cell.row * size

    def update(self):
        state = LightsCellSprite.RED if (self.cell.lights == Lights.CARS_RED) else LightsCellSprite.GREEN
        self.image = pygame.transform.scale(self.originals[state], (self.size, self.size))
        self.image.set_colorkey((255, 255, 255))