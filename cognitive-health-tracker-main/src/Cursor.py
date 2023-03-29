import pygame
import global_variables as gv

windowHeightOffset = 0


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super(Cursor, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((153, 186, 128))
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys, width, height):
        if pressed_keys[gv.K_UP]:
            self.rect.move_ip(0, -1)
        if pressed_keys[gv.K_DOWN]:
            self.rect.move_ip(0, 1)
        if pressed_keys[gv.K_LEFT]:
            self.rect.move_ip(-1, 0)
        if pressed_keys[gv.K_RIGHT]:
            self.rect.move_ip(1, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width-windowHeightOffset:
            self.rect.right = width-windowHeightOffset
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= height-windowHeightOffset:
            self.rect.bottom = height-windowHeightOffset

    # Not sure what this is - Darren you used in Saccade?
    def update_m(self, m_pos1, m_pos2):
        self.rect.x = m_pos1
        self.rect.y = m_pos2
