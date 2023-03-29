import pygame

class Box(pygame.sprite.Sprite):
    type = ''
    value = 0
    length = 0
    width = 0

    def __init__(self):
        super(Box, self).__init__()
        self.font=pygame.font.SysFont('Times New Roman',20)
        self.surf = pygame.Surface((120, 50))
        #self.surf.fill((153, 186, 128))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

    def update(self, x, y):
        # updates hitbox coords
        self.rect.y = y
        self.rect.x = x
        self.length=x
        self.width=y

    def addText(self, text, x, y):
        self.surf.blit(self.font.render(text, True, (0, 0, 0)), (x, y))
        pygame.display.update()

    def changeSize(self, x, y):
        self.surf=pygame.Surface((x, y))

    def changeColor(self, r, g, b):
        self.surf.fill((r, g, b))

    def removeText(self, text, x, y):
        self.surf.blit(self.font.render(text, True, (153, 186, 128)), (x, y))
        pygame.display.update()
