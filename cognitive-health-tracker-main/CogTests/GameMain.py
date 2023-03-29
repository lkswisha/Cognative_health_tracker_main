import pygame
import sys
import random
import csv

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

#Colors
black = (0,0,0)
gray = (143,143,143)
white = (255,255,255)
class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super(Cursor, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill(black)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -1)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 1)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-1, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(1, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 500:
            self.rect.right = 500
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= 500:
            self.rect.bottom = 500

    def update_m(self, m_pos1, m_pos2):
        self.rect.x = m_pos1
        self.rect.y = m_pos2


class Box(pygame.sprite.Sprite):
    def __init__(self):
        super(Box, self).__init__()
        self.surf = pygame.Surface((100, 50))
        self.surf.fill((153, 186, 128))
        self.rect = self.surf.get_rect()

    def update(self, x, y):
        # updates hitbox coords
        self.rect.y = y
        self.rect.x = x


class Circle(pygame.sprite.Sprite):
    def __init__(self):
        super(Circle, self).__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(white)  # # rectangle is 'invisible'
        self.rect = self.image.get_rect()
        self.color = black
        pygame.draw.circle(self.image, self.color, (25, 25), 25)

    def update(self, x, y, c):
        # updates hitbox coords and circle color
        self.rect.y = y
        self.rect.x = x
        pygame.draw.circle(self.image, c, (25, 25), 25)

def write_to_CSV(value):
    read_list = []
    with open('C:/Users/darre/Documents/Temp_Database/data.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            read_list.append(row)
    with open('C:/Users/darre/Documents/Temp_Database/data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        i = 0
        for row in read_list:
            row.append(value[i])
            i += 1
            writer.writerow(row)

def Saccade():
    pygame.init()
    screen = pygame.display.set_mode([500, 500])
    # index 0-1 for one circle, 2-3 for other circle
    positions = [[200, 100, 200, 300], [400, 200, 0, 200], [300, 150, 100, 250], [300, 250, 100, 150]]  # #| - / \
    # positions_f = [[200, 300], [0, 200], [100, 250], [100, 150]]  # #| - / \ opposite coords as positions
    cursor = Cursor()
    static = Circle()
    circle = Circle()
    flash = Circle()
    flash_color = [gray, black]
    fc_index = 0

    ROI_sprites = pygame.sprite.Group()
    ROI_sprites.add(flash)  # # for round 1

    ROI_sprites_p2 = pygame.sprite.Group()
    ROI_sprites_p2.add(circle)  # # for round 2

    # private variables
    change_orientation = True
    run = True
    random.shuffle(positions)
    pos_index = 0
    indices1 = [0, 1]
    indices2 = [2, 3]
    cursor_hold_counter = 0
    round_counter = 0
    score_list = []

    # clock
    clock = pygame.time.Clock()
    clock.tick(10)  # game fps
    prev_ticks = pygame.time.get_ticks()  # #start game tick count
    round_timer_start = pygame.time.get_ticks()

    # text
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Pick the FLASHING dot', True, (0, 0, 128), (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (220, 20)

    # progress bar
    progress_bar = pygame.image.load("progress bar.png")
    progress_bar_rect = progress_bar.get_rect(topleft=(30, 450))
    progress_bar_width = 50

    while run:
        # start timer for player time
        # decide the orientation
        if change_orientation:
            pos_index += 1
            change_orientation = False
            if pos_index > 3:
                random.shuffle(positions)  # # re-shuffle the positions
                # swap indices
                temp_indices = indices2
                temp_indices2 = indices1
                indices2 = temp_indices2
                indices1 = temp_indices
                pos_index = 0  # # reset the index
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        screen.fill(white)
        # progress bar
        if round_counter < 16:

            progress_bar = pygame.transform.scale(progress_bar, (round_counter*27, 30))
            progress_bar_rect = progress_bar.get_rect(topleft=(30, 450))
            screen.blit(progress_bar, progress_bar_rect)

        # Center Dot
        static.update(200, 200, black)
        screen.blit(static.image, [200, 200])

        # Draw ROI on screen
        circle.update(positions[pos_index][indices1[0]], positions[pos_index][indices1[1]], black)
        screen.blit(circle.image, [positions[pos_index][indices1[0]], positions[pos_index][indices1[1]]])

        flash.color = gray
        # flash.update(positions[pos_index][2], positions[pos_index][3], flash_color[fc_index])
        ROI_sprites.update(positions[pos_index][indices2[0]], positions[pos_index][indices2[1]], flash_color[fc_index])
        screen.blit(flash.image, [positions[pos_index][indices2[0]], positions[pos_index][indices2[1]]])
        # swap the colors every 300 ms
        if pygame.time.get_ticks() >= prev_ticks+300:
            prev_ticks = pygame.time.get_ticks()
            if fc_index == 0:
                fc_index = 1
            else:
                fc_index = 0

        # Draw cursor on the screen
        screen.blit(cursor.surf, cursor.rect)
        # Update the player sprite based on user keypresses
        #pressed_keys = pygame.key.get_pressed()
        #cursor.update(pressed_keys)
        cursor.update_m(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        if round_counter < 8:
            screen.blit(text, textRect)
            if pygame.sprite.spritecollideany(cursor, ROI_sprites):
                cursor.surf.fill(gray)
                cursor_hold_counter += 1
                if cursor_hold_counter == 5000:
                    change_orientation = True
                    round_counter += 1

                    round_timer_end = pygame.time.get_ticks()
                    round_score = (round_timer_end - round_timer_start) / 1000  # player time score and convert ticks to seconds
                    round_timer_start = pygame.time.get_ticks()
                    print(round_score)  # temporary
                    score_list.append(round_score)

            else:
                cursor.surf.fill(black)
                if cursor_hold_counter > 0:
                    cursor_hold_counter -= 2
        elif round_counter >= 8 and round_counter < 16:
            # swap to non_blinking
            text = font.render('Pick the NON-FLASHING dot', True, (0, 0, 128), (255, 255, 255))
            screen.blit(text, textRect)
            if pygame.sprite.spritecollideany(cursor, ROI_sprites_p2):
                cursor.surf.fill(gray)
                cursor_hold_counter += 1
                if cursor_hold_counter == 5000:
                    change_orientation = True
                    round_counter += 1

                    round_timer_end = pygame.time.get_ticks()
                    round_score = (round_timer_end - round_timer_start) / 1000  # player time score and convert ticks to seconds
                    round_timer_start = pygame.time.get_ticks()
                    print(round_score)  # temporary
                    score_list.append(round_score)

            else:
                cursor.surf.fill(black)
                if cursor_hold_counter > 0:
                    cursor_hold_counter -= 2
        # Update the display
        else:
            run = False
        pygame.display.flip()

    # end of game functionality
    pygame.quit()
    write_to_CSV(score_list)
    return sum(score_list)  # return the sum of the elements in score_list for total time

Saccade()
