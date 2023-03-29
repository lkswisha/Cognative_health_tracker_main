import pygame

class Circle(pygame.sprite.Sprite):
    def __init__(self):
        super(Circle, self).__init__()
        self.image = pygame.Surface((100, 100))
        self.image.fill((226, 230, 223))  # # rectangle is 'invisible'
        self.rect = self.image.get_rect()
        self.color = (153, 186, 128)
        pygame.draw.circle(self.image, self.color, (50, 50), 50)

    def update(self, x, y, c):
        # updates hitbox coords and circle color
        self.rect.y = y
        self.rect.x = x
        pygame.draw.circle(self.image, c, (50, 50), 50)
