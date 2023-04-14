import pygame
import random
import math
import numpy as np
import pyautogui
import os
import global_variables as gv
import Cursor
import time
import threading

#Seeing if Git works for me too
#Just commit

"""
Object of interest.
"""
class Node(pygame.sprite.Sprite):
    def __init__(self, img, val, idx):
        super(Node, self).__init__()
        self.image = pygame.image.load(img)
        #self.image.fill((226, 230, 223))  # 'invisible'
        self.rect = self.image.get_rect()
        self.color = (153, 186, 128)
        self.value = val
        self.index = idx
        self.selected = False

    # # called when game updates the node object
    def update(self, x, y, c):
        self.rect.y = y
        self.rect.x = x
        #pygame.draw.circle(self.image, c, (25, 25), 25)

#timer = None
def mouse_function():
    #global timer
    print("Mouse location during Test")
    print(pyautogui.position())
    #timer = threading.Timer(0.5,mouse_function())
    #timer.start
    #time.sleep(0.25)
    '''the time sleep aspect cuts down to a manageable number of data points but because of where the function 
    is implemented in the code it causes the cursor to lag at the sleep time 
    *next step is to print this to a csv instead of run terminal'''

def draw_circle(n):
    # (x-h)^2 + (y-k)^2 = r^2
    # x = r * cos(theta) + h
    # y = r - sin(theta) + k

    h = gv.SCREEN_WIDTH / 2.4  # these values are simply tested values to adjust the coordinates of the circle properly
    k = gv.SCREEN_HEIGHT / 2.7
    r = 200  # radius of circle

    positions = []
    step_size = (2 * math.pi) / n
    theta = 0

    # generate orientation mapping into circle shape
    while theta < 2 * math.pi:
        positions.append((r * math.cos(theta) + h, r * math.sin(theta) + k))
        theta += step_size

    return positions


class TrailBlazerTest:
    def __init__(self, eye_tracking=False):
        self.eye_tracking = eye_tracking
        self.eye_tracker = None
        self.num_of_incorrect = 0
        self.total_time = 0
        self.frame_counter = 0
        self.current_pos = pyautogui.position()
        self.mouse_location = []

    def setTotalTime(self,time):
        self.total_time = time

    def getTotalTime(self):
        return self.total_time

    def setNumOfIncorrect(self,incorrect):
        self.num_of_incorrect = incorrect

    def setMouseLocation(self, m_l):
        self.mouse_location = m_l

    def getNumOfIncorrect(self):
        return self.num_of_incorrect

    def getMouseLocation(self):
        return self.mouse_location

    """
    Game Logic
    """
    def rules(self):
        # Find the ground truth
        # During play, keep track of nodes chosen and keep in list

        # Either correct node by node
        # or
        # Check entire list
        return

    """
    Callback function for gaze data. 
    """
    def gaze_data_callback(self, gaze_data):
        self.frame_counter += 1
        print("papasito")
        max_len = 10
        if self.frame_counter >= max_len:
            print("Left eye: ({gaze_left_eye}) \t Right eye: ({gaze_right_eye})".format(
                gaze_left_eye=gaze_data['left_gaze_point_on_display_area'],
                gaze_right_eye=gaze_data['right_gaze_point_on_display_area']))

            left_gaze = gaze_data['left_gaze_point_on_display_area']
            right_gaze = gaze_data['right_gaze_point_on_display_area']

            if (np.isnan(left_gaze[0]) and np.isnan(left_gaze[1])) or (np.isnan(right_gaze[0]) and np.isnan(right_gaze[1])):
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
                speed = 0.25  # [s]econds
                #pyautogui.moveTo(avg_x, avg_y, duration=speed)

                # Reset
                self.frame_counter = 0

        # print("x: {0}, y: {1}".format(x, y))
        # print("Left eye: ({gaze_left_eye}) \t Right eye: ({gaze_right_eye})".format(
        #     gaze_left_eye=x,
        #     gaze_right_eye=y))

    """
    Validate the user's choice
    """
    def validate(self, node, ground_truth):
        # Compare the user's choice with the answer key
        index = ground_truth["index"]
        if node.value == ground_truth["answer"][index]:
            ground_truth["index"] += 1
            return True
        return False

    """
    TrailBlazer Test
    """
    def TrailBlazer(self, num_of_nodes, numbers=False, alpha_numeric=False):
        pygame.init()
        prev_value = 0 #keep track of previous node value
        #instructions.create_instructions("TrailBlazer")

        screen = pygame.display.set_mode([gv.SCREEN_WIDTH, gv.SCREEN_HEIGHT])
        pygame.display.set_caption("TrailBlazer baby!")
        positions = draw_circle(num_of_nodes)  # TODO - limit number of nodes to the amount of icons we have - e.g. if /
        # the user wants 10 nodes, but we only have 8 images.

        random.shuffle(positions)  # randomize the nodes

        ground_truth = {
            "index": 0,
            "answer": []
        }

        # Generate nodes
        nodes = {}
        all_nodes = pygame.sprite.Group()
        img_dir = os.path.join(gv.path_to_images, "trailblazer")

        if numbers is True:
            img_dir = os.path.join(img_dir, "Numbers")
        else:
            img_dir = os.path.join(img_dir, "Letters")

        # TODO - implement alphanumberic implementation

        all_imgs = os.listdir(img_dir)

        for i in range(num_of_nodes):
            idx = random.randrange(0, len(all_imgs))     # Generate random number
            curr_node = "node{0}".format(i)
            curr_img = all_imgs.pop(idx)
            img_path = os.path.join(img_dir, curr_img)   # Full path to image
            curr_img = os.path.splitext(curr_img)[0]     # Get filename w/o extension
            value = int(curr_img) if numbers is True else ord(curr_img)
            nodes[curr_node] = Node(img_path, value, i)  # Create node
            all_nodes.add(nodes[curr_node])              # Add node to sprite group
            ground_truth["answer"].append(value)         # Generate the ground truth

        ground_truth["answer"].sort()

        cursor = Cursor.Cursor()
        MAX_GAME_TIME = 300  # [s]econds
        start_time = pygame.time.get_ticks()
        total_time = 0
        time_elapsed = 0
        initial_hold_time = 0
        time_to_select_ans = 1000

        user_choice = set() # Created to track user's answers. Do we still need?
        incorrect = 0

        if self.eye_tracking:
            self.eye_tracker = EyeTracking.camera.Camera()
            self.eye_tracker.find_eyetrackers()
            self.eye_tracker.start_gaze_data(self.gaze_data_callback)

        mouse_location = []
        running = True
        while running:
            mouse_location.append(pyautogui.position())
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    if self.eye_tracking and self.eye_tracker is not None:
                        self.eye_tracker.stop_gaze_data()  # Unsubscribe from capturing gaze data

            # Check to see if the eyetracker is connected and turned on
            if self.eye_tracking and self.eye_tracker is None:
                raise ValueError("Lost connection with eye tracker. Stopping the game...")

            time_elapsed = (pygame.time.get_ticks() - start_time)/1000

            # User took too long --> stop the game
            if time_elapsed >= MAX_GAME_TIME:
                pygame.quit()

            screen.fill((226, 230, 223))

            # Draw ROI on screen
            index = 0
            for i in range(num_of_nodes):
                curr_node = nodes["node{0}".format(i)]
                curr_node.update(positions[curr_node.index][0], positions[curr_node.index][1], (153, 186, 128))
                if curr_node.selected is True:
                    pygame.draw.circle(screen, (0, 255, 0),
                                       (positions[curr_node.index][0]+50, positions[curr_node.index][1]+50), 50)

                screen.blit(curr_node.image, [positions[index][0], positions[index][1]])
                index += 1

            # Use eye tracking coordinates
            if self.eye_tracking:
                cursor.rect.x = self.current_pos[0]
                cursor.rect.y = self.current_pos[1]

            # Draw cursor on the screen
            screen.blit(cursor.surf, cursor.rect)

            #timer = threading.Timer(0.5,mouse_function())
            #timer.start()
            #input()
            mouse_function()

            # Update the player sprite based on mouse
            if self.eye_tracking:
                print("update cursor to ({0})".format(self.current_pos))
                cursor.update_m(self.current_pos[0], self.current_pos[1])
            else:
                cursor.update_m(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

            # Update the display
            pygame.display.flip()

            # If collision occurred, return the node where collision occurred
            collided_node = pygame.sprite.spritecollideany(cursor, all_nodes)
            if collided_node:
                #mouse_function()
                cursor.surf.fill(gv.gold)
                if initial_hold_time == 0:
                    initial_hold_time = pygame.time.get_ticks()  # clock the time

                time_elapsed = pygame.time.get_ticks() - initial_hold_time
                if time_elapsed > time_to_select_ans:
                    initial_hold_time = 0
                    user_choice.add(collided_node)

                    # Validate user's answer
                    if self.validate(collided_node, ground_truth):
                        collided_node.selected = True
                        all_nodes.remove(collided_node)
                        print("Correct Answer")
                        if len(all_nodes.sprites()) == 0:
                            running = False
                            if self.eye_tracking and self.eye_tracker is not None:
                                self.eye_tracker.stop_gaze_data()  # Unsubscribe from capturing gaze data
                    else:
                        # variables to draw circle to indicate error
                        r = 48  # radius
                        a = positions[collided_node.index][0] + 50  # center x coordinate
                        b = positions[collided_node.index][1] + 50  # center y coordinate

                        clock = pygame.time.Clock()
                        for i in range(1, 361):
                            clock.tick(1000)
                            pygame.draw.circle(screen, (255, 0, 0),
                                               (int(r * math.cos(math.radians(i)) + a), int(r * math.sin(math.radians(i)) + b)), 3)
                            pygame.display.update()

                        if prev_value != collided_node.value:
                            # Tell user it was wrong
                            incorrect += 1
                            print("Wrong answer")
                            prev_value = collided_node.value

                    pygame.display.update()
            else:
                initial_hold_time = 0
                cursor.surf.fill(gv.black)

        self.setMouseLocation(mouse_location)
        self.setNumOfIncorrect(incorrect)
        self.setTotalTime(time_elapsed)
        pygame.quit()
        return 1


testing = False
if testing:
    eye_tracking = False
    tb = TrailBlazerTest(eye_tracking)
    tb.TrailBlazer(7)
