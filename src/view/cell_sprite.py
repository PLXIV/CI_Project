import pygame


class CellSprite(pygame.sprite.Sprite):

    def __init__(self, image, size, x, y, row, col):
        pygame.sprite.Sprite.__init__(self)
        self.original = image
        self.row = row
        self.col = col

        if image is None:
            self.image = pygame.Surface([size, size])
            self.image.fill((0, 0, 0))
        else:
            self.image = pygame.transform.scale(self.original, (size, size))
            self.image.set_colorkey((255, 255, 255))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def resize(self, size, x, y):
        if self.original is None:
            self.image = pygame.Surface([size, size])
            self.image.fill((0, 0, 0))
        else:
            self.image = pygame.transform.scale(self.original, (size, size))
            self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y