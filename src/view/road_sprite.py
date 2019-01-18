import pygame


class RoadSprite(pygame.sprite.Sprite):

    def __init__(self, color, width, height, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y