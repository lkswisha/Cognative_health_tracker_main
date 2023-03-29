import os
import pyautogui

"""
Set up path to images.
Differs depending on working directory.
"""
path_to_results = ""
path_to_images = ""
cwd = os.getcwd()
if cwd.endswith("CogTests"):
    path_to_images = "..\\images\\"
else:
    path_to_images = ".\\images\\"

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
# Window dimensions
SCREEN_SIZE = pyautogui.size()
SCREEN_WIDTH, SCREEN_HEIGHT = (SCREEN_SIZE.width, SCREEN_SIZE.height)

# Colors
black = (0,0,0)
gray = (143,143,143)
white = (255,255,255)
gold = (240, 194, 70)
