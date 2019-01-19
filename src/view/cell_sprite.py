import pygame


class CellSprite(pygame.sprite.Sprite):

    def __init__(self, image, size, cell, margin_w, margin_h):
        pygame.sprite.Sprite.__init__(self)
        self.original = image
        self.cell = cell
        self.margin_w = margin_w
        self.margin_h = margin_h
        self.size = size

        if image is None:
            self.image = pygame.Surface([size, size])
            self.image.fill((0, 0, 0))
        else:
            self.image = pygame.transform.scale(self.original, (size, size))
            self.image.set_colorkey((255, 255, 255))

        self.rect = self.image.get_rect()
        self.rect.x = margin_w + cell.col * size
        self.rect.y = margin_h + cell.row * size

    def resize(self, size, margin_w, margin_h):
        if self.original is None:
            self.image = pygame.Surface([size, size])
            self.image.fill((0, 0, 0))
        else:
            self.image = pygame.transform.scale(self.original, (size, size))
            self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = margin_w + self.cell.col * size
        self.rect.y = margin_h + self.cell.row * size