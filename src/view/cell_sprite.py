import pygame


class CellSprite(pygame.sprite.Sprite):

    def __init__(self, image, width, height, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.original = image

        if image is None:
            self.image = pygame.Surface([width, height])
            self.image.fill((0, 0, 0))
        else:
            self.image = pygame.transform.scale(self.original, (width, height))
            self.image.set_colorkey((255, 255, 255))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y