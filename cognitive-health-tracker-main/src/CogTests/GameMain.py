import pygame
import sys
import random
import csv
import pyautogui
import numpy as np
from datetime import date
import os
import global_variables as gv
import Box
import Cursor
import Circle
import time
#import instructions


TimerOffset=1000
"""
def write_to_CSV(value):
    read_list = []
    with open('C:/Users/user/Documents/Temp_Database/data.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            read_list.append(row)
    with open('C:/Users/user/Documents/Temp_Database/data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        i = 0
        for row in read_list:
            row.append(value[i])
            i += 1
            writer.writerow(row)
"""

"""
Writes input value into CSV file
@param value array of values to be written in to CSV
@returns success
"""
def mouse_function():
    print("Mouse location during Test")
    print(pyautogui.position())
    #time.sleep(1)
    '''Time.sleep makes the whole test glitch'''

def write_to_CSV(value):
    with open('data.csv', 'a+', newline='') as file_credentials:
        file_credentials.seek(0)
        writer=csv.DictWriter(file_credentials,fieldnames=['Date','Test','Round 1','Round 2','Round 3','Round 4',
                                                           'Round 5','Round 6','Round 7','Round 8','Round 9',
                                                           'Round 10','Round 11','Round 12','Round 13','Round 14',
                                                           'Round 15','Round 16'])
        writer.writeheader()
        today=date.today()
        writer.writerow({'Date': today.strftime('%d/%m/%Y'),'Test':'Vip','Round 1':value[0],'Round 2':value[1],'Round 3':value[2],'Round 4':value[3],
                                                           'Round 5':value[4],'Round 6':value[5],'Round 7':value[6],
                                                            'Round 8':value[7],'Round 9':value[8],
                                                           'Round 10':value[9],'Round 11':value[10],'Round 12':value[11],
                                                            'Round 13':value[12],'Round 14':value[13],
                                                           'Round 15':value[14],'Round 16':value[15]})
        #file_credentials.flush()
        return 1


"""
Class Definition for whole Saccade Test and its parts
"""
class SaccadeTest:
    """
    Self definition of variables
    """
    def __init__(self, user, eye_tracking=False):
        self.results = []
        self.user = user
        self.eye_tracking = eye_tracking
        self.eye_tracker = None
        self.frame_counter = 0
        self.current_pos = pyautogui.position()

    # # Exposeses results to other functions
    def getResults(self):
        return self.results

    # # maps gaze data to screen coordinate
    def gaze_data_callback(self, gaze_data):
        self.frame_counter += 1
        print("papasito")
        max_len = 10
        if self.frame_counter >= max_len:
            # Print gaze points of left and right eye

            print("Left eye: ({gaze_left_eye}) \t Right eye: ({gaze_right_eye})".format(
                gaze_left_eye=gaze_data['left_gaze_point_on_display_area'],
                gaze_right_eye=gaze_data['right_gaze_point_on_display_area']))

            left_gaze = gaze_data['left_gaze_point_on_display_area']
            right_gaze = gaze_data['right_gaze_point_on_display_area']

            if (np.isnan(left_gaze[0]) and np.isnan(left_gaze[1])) or (
                    np.isnan(right_gaze[0]) and np.isnan(right_gaze[1])):
                monitor_pixels = (np.nan, np.nan)
                return monitor_pixels

            left_gaze = (
                int(left_gaze[0] * gv.SCREEN_WIDTH),
                int(left_gaze[1] * gv.SCREEN_HEIGHT)
            )
            right_gaze = (
                int(right_gaze[0] * gv.SCREEN_WIDTH),
                int(right_gaze[1] * gv.SCREEN_HEIGHT)
            )

            # Take the average of the left and right eye coordinates , not monocular friendly
            avg_x = (left_gaze[0] + right_gaze[0]) / 2
            avg_y = (left_gaze[1] + right_gaze[1]) / 2

            # Are coordinates valid?
            print("x: {0} , y: {1}".format(avg_x, avg_y))
            if avg_x >= 0 and avg_y >= 0:
                # Save current position
                print("old position = {0}".format(self.current_pos))
                self.current_pos = [avg_x, avg_y]
                print("new position = {0}".format(self.current_pos))

                # As per documentation, setting duration < pyautogui.MINIMUM_DURATION makes it move instantaneously
                speed = 0.25  # [s]
                # pyautogui.moveTo(avg_x, avg_y, duration=speed)

                # Reset
                self.frame_counter = 0

    """
    Function definition for Saccade Test runner
    """
    def Saccade(self):
        # pygame engine
        pygame.init()
        #instructions.create_instructions("Saccade")

        screen = pygame.display.set_mode([gv.SCREEN_WIDTH, gv.SCREEN_HEIGHT])
        # index 0-1 for one circle, 2-3 for other circle
        positions = [[gv.SCREEN_WIDTH * 0.4, gv.SCREEN_HEIGHT * 0.2, gv.SCREEN_WIDTH * 0.4, gv.SCREEN_HEIGHT * 0.6],
                     [gv.SCREEN_WIDTH * 0.8, gv.SCREEN_HEIGHT * 0.4, gv.SCREEN_WIDTH * 0.2, gv.SCREEN_HEIGHT * 0.4],
                     #changed 3rd location to not zero so its not on the edge of the monitor
                     [gv.SCREEN_WIDTH * 0.6, gv.SCREEN_HEIGHT * 0.3, gv.SCREEN_WIDTH * 0.2, gv.SCREEN_HEIGHT * 0.5],
                     [gv.SCREEN_WIDTH * 0.6, gv.SCREEN_HEIGHT * 0.5, gv.SCREEN_WIDTH * 0.2, gv.SCREEN_HEIGHT * 0.3]]  # #| - / \
        # positions_f = [[200, 300], [100, 200], [100, 250], [100, 150]]  # #| - / \ opposite coords as positions
        cursor = Cursor.Cursor()
        static = Box.Box()
        continueBox = Box.Box()
        circle = Circle.Circle()
        flash = Circle.Circle()
        flash_color = [gv.gray, gv.black]
        fc_index = 0

        ROI_sprites = pygame.sprite.Group()
        ROI_sprites.add(flash)  # # for round 1

        ROI_sprites_p2 = pygame.sprite.Group()
        ROI_sprites_p2.add(circle)  # # for round 2

        ROI_sprites_continue = pygame.sprite.Group()
        ROI_sprites_continue.add(continueBox)

        # private variables
        change_orientation = True
        run = True
        random.shuffle(positions)
        pos_index = 0
        indices1 = [0, 1]
        indices2 = [2, 3]
        total_hold_time = 2000  # ms
        initial_hold_time = 0
        round_counter = 0
        score_list = []

        # clock
        clock = pygame.time.Clock()
        clock.tick(10)  # game fps
        prev_ticks = pygame.time.get_ticks()  # #start game tick count
        round_timer_start = pygame.time.get_ticks()

        # text
        font = pygame.font.SysFont('times.ttf', 32)
        #text = font.render('Pick the FLASHING dot', True, (0, 0, 128), (255, 255, 255))
        #textRect = text.get_rect()
        #textRect.center = (gv.SCREEN_WIDTH*0.44, gv.SCREEN_HEIGHT*0.04)

        # progress bar
        progress_bar = pygame.image.load(gv.path_to_images + "progress bar.png")
        progress_bar_rect = progress_bar.get_rect(topleft=(gv.SCREEN_WIDTH*0.06, gv.SCREEN_HEIGHT*0.9))
        progress_bar_width = gv.SCREEN_WIDTH*0.1

        if self.eye_tracking:
            self.eye_tracker = camera.Camera()
            self.eye_tracker.find_eyetrackers()
            self.eye_tracker.start_gaze_data(self.gaze_data_callback)

        # # main game logic loop
        while run:
            mouse_function()
            # # end game engine if quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    if self.eye_tracking and self.eye_tracker is not None:
                        self.eye_tracker.stop_gaze_data() # Unsubscribe from capturing gaze data

            # Check to see if the eyetracker is connected and turned on
            if self.eye_tracking and self.eye_tracker is None:
                raise ValueError("Lost connection with eye tracker. Stopping the game...")

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

            screen.fill(gv.white)
            # progress bar
            if round_counter < 18:
                progress_bar = pygame.transform.scale(progress_bar,
                                                      (round_counter * gv.SCREEN_WIDTH * 0.054, gv.SCREEN_HEIGHT * 0.06))
                progress_bar_rect = progress_bar.get_rect(topleft=(gv.SCREEN_WIDTH * 0.06, gv.SCREEN_HEIGHT * 0.9))
                screen.blit(progress_bar, progress_bar_rect)

            # Center Dot
            # Center Square
            static.changeSize(50, 50)
            static.update(gv.SCREEN_WIDTH * 0.4, gv.SCREEN_HEIGHT * 0.4)
            static.changeColor(0, 0, 0)
            screen.blit(static.surf, (gv.SCREEN_WIDTH * 0.4, gv.SCREEN_HEIGHT * 0.4))

            # Draw ROI on screen
            circle.update(positions[pos_index][indices1[0]], positions[pos_index][indices1[1]], gv.black)
            screen.blit(circle.image, [positions[pos_index][indices1[0]], positions[pos_index][indices1[1]]])

            flash.color = gv.gray
            # flash.update(positions[pos_index][2], positions[pos_index][3], flash_color[fc_index])
            ROI_sprites.update(positions[pos_index][indices2[0]], positions[pos_index][indices2[1]],
                               flash_color[fc_index])
            screen.blit(flash.image, [positions[pos_index][indices2[0]], positions[pos_index][indices2[1]]])
            # swap the colors every 300 ms
            if pygame.time.get_ticks() >= prev_ticks + 300:
                prev_ticks = pygame.time.get_ticks()
                if fc_index == 0:
                    fc_index = 1
                else:
                    fc_index = 0

            # Use eye tracking coordinates
            if self.eye_tracking:
                cursor.rect.x = self.current_pos[0]
                cursor.rect.y = self.current_pos[1]

            # Draw cursor on the screen
            screen.blit(cursor.surf, cursor.rect)

            # Update the player sprite based on user keypresses
            # pressed_keys = pygame.key.get_pressed()
            # cursor.update(pressed_keys)
            if self.eye_tracking:
                print("update cursor to ({0})".format(self.current_pos))
                cursor.update_m(self.current_pos[0], self.current_pos[1])
            else:
                cursor.update_m(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

            # # handles rounds for flashing dot
            if round_counter==0:
                screen.fill(gv.white)
                font = pygame.font.SysFont('times.ttf', 48)
                text = font.render(
                    'For the first half you will hover over the Flashing Dots. Hover over the continue box to continue the test.',
                    True, (0, 0, 128), (255, 255, 255))
                screen.blit(text, (gv.SCREEN_WIDTH * 0.05, gv.SCREEN_HEIGHT * 0.4))
                ROI_sprites_continue.update(gv.SCREEN_WIDTH * 0.5, gv.SCREEN_HEIGHT * 0.6)
                continueBox.update(gv.SCREEN_WIDTH * 0.5, gv.SCREEN_HEIGHT * 0.6)
                continueBox.changeColor(83, 83, 83)
                screen.blit(continueBox.surf, (gv.SCREEN_WIDTH * 0.5, gv.SCREEN_HEIGHT * 0.6))
                font = pygame.font.SysFont('times.ttf', 32)
                text = font.render("Continue", True, (255, 255, 255))
                textRect = text.get_rect()
                textRect.topleft = (gv.SCREEN_WIDTH * 0.5, gv.SCREEN_HEIGHT * 0.6)
                screen.blit(text, textRect)
                if pygame.sprite.spritecollideany(cursor, ROI_sprites_continue):
                    cursor.surf.fill(gv.black)
                    if initial_hold_time == 0:
                        initial_hold_time = pygame.time.get_ticks()  # clock the timer
                    time_elapsed = pygame.time.get_ticks() - initial_hold_time
                    if time_elapsed > total_hold_time:
                        change_orientation = True
                        round_counter += 1
                        print("added counter")
                        initial_hold_time = 0
            elif round_counter < 9:
                screen.blit(text, textRect)
                if pygame.sprite.spritecollideany(cursor, ROI_sprites):
                    cursor.surf.fill(gv.gray)
                    if initial_hold_time == 0:
                        initial_hold_time = pygame.time.get_ticks()  # clock the timer
                    time_elapsed = pygame.time.get_ticks() - initial_hold_time
                    if time_elapsed > total_hold_time:
                        change_orientation = True
                        round_counter += 1

                        round_timer_end = pygame.time.get_ticks()
                        round_score = (
                                                  round_timer_end - round_timer_start) / 1000  # player time score and convert ticks to seconds
                        round_timer_start = pygame.time.get_ticks()
                        print(round_score)  # temporary
                        score_list.append(round_score)
                        initial_hold_time=0
                else:
                    initial_hold_time = 0
                    cursor.surf.fill(gv.black)
            elif round_counter==9:
                screen.fill(gv.white)
                font = pygame.font.SysFont('times.ttf', 48)
                text = font.render('For the second half you will hover over the Non Flashing Dots. Hover over the continue box to continue the test.', True, (0, 0, 128), (255, 255, 255))
                screen.blit(text, (gv.SCREEN_WIDTH*0.05,gv.SCREEN_HEIGHT*0.4))
                ROI_sprites_continue.update(gv.SCREEN_WIDTH*0.5,gv.SCREEN_HEIGHT*0.6)
                continueBox.update(gv.SCREEN_WIDTH*0.5,gv.SCREEN_HEIGHT*0.6)
                continueBox.changeColor(83,83,83)
                screen.blit(continueBox.surf,(gv.SCREEN_WIDTH*0.5,gv.SCREEN_HEIGHT*0.6))
                font = pygame.font.SysFont('times.ttf', 32)
                text = font.render("Continue", True, (255,255,255))
                textRect = text.get_rect()
                textRect.topleft = (gv.SCREEN_WIDTH*0.5, gv.SCREEN_HEIGHT*0.6)
                screen.blit(text, textRect)
                if pygame.sprite.spritecollideany(cursor,ROI_sprites_continue):
                    cursor.surf.fill(gv.black)
                    if initial_hold_time == 0:
                        initial_hold_time = pygame.time.get_ticks()  # clock the timer
                    time_elapsed = pygame.time.get_ticks() - initial_hold_time
                    if time_elapsed > total_hold_time:
                        change_orientation = True
                        round_counter += 1
                        print("added counter")
                        initial_hold_time = 0

            # # handles rounds for non-flashing dot
            elif round_counter > 9 and round_counter < 18:
                # swap to non_blinking
                #text = font.render('Pick the NON-FLASHING dot', True, (0, 0, 128), (255, 255, 255))
                #screen.blit(text, textRect)
                if pygame.sprite.spritecollideany(cursor, ROI_sprites_p2):
                    cursor.surf.fill(gv.gray)
                    if initial_hold_time == 0:
                        initial_hold_time = pygame.time.get_ticks()  # clock the timer
                    time_elapsed = pygame.time.get_ticks() - initial_hold_time
                    if time_elapsed > total_hold_time:
                        change_orientation = True
                        round_counter += 1

                        round_timer_end = pygame.time.get_ticks()
                        round_score = (round_timer_end - round_timer_start) / 1000  # player time score and convert ticks to seconds
                        round_timer_start = pygame.time.get_ticks()
                        print(round_score)  # temporary
                        score_list.append(round_score)
                        initial_hold_time=0
                else:
                    initial_hold_time = 0
                    cursor.surf.fill(gv.black)

                    """
                    cursor_hold_counter += 1
                    if cursor_hold_counter == 5000:
                        change_orientation = True
                        round_counter += 1

                        round_timer_end = pygame.time.get_ticks()
                        round_score = (
                                                  round_timer_end - round_timer_start) / 1000  # player time score and convert ticks to seconds
                        round_timer_start = pygame.time.get_ticks()
                        print(round_score)  # temporary
                        score_list.append(round_score)

                else:
                    cursor.surf.fill(gv.black)
                    if cursor_hold_counter > 0:
                        cursor_hold_counter -= 2
            elif round_counter >= 8 and round_counter < 16:
                # swap to non_blinking
                text = font.render('Pick the NON-FLASHING dot', True, (0, 0, 128), (255, 255, 255))
                screen.blit(text, textRect)
                if pygame.sprite.spritecollideany(cursor, ROI_sprites_p2):
                    cursor.surf.fill(gv.gray)
                    cursor_hold_counter += 1
                    if cursor_hold_counter == 5000:
                        change_orientation = True
                        round_counter += 1

                        round_timer_end = pygame.time.get_ticks()
                        round_score = (
                                                  round_timer_end - round_timer_start) / 1000  # player time score and convert ticks to seconds
                        round_timer_start = pygame.time.get_ticks()
                        print(round_score)  # temporary
                        score_list.append(round_score)

                else:
                    cursor.surf.fill(gv.black)
                    if cursor_hold_counter > 0:
                        cursor_hold_counter -= 2
            """
            # Update the display
            else:
                run = False
                if self.eye_tracking and self.eye_tracker is not None:
                    self.eye_tracker.stop_gaze_data()  # Unsubscribe from capturing gaze data
            pygame.display.flip()

        # end of game functionality
        pygame.quit()
        #write_to_CSV(score_list)
        self.results=score_list
        #return sum(score_list)
        return 1  # so that it doesn't stall while py!=1: pass in main.py

# # solo test of function
testing = False
if testing:
    eye_tracking = False
    s = SaccadeTest("test", eye_tracking)
    s.Saccade()
