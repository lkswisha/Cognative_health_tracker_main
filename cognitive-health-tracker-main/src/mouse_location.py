import csv
import pandas as pd
import os
import sys

def mouse_function():
    print("Mouse location during Test")
    print(os.path.join(sys.path[0], "my_file.txt"))
    #print(pyautogui.position())
    '''Time.sleep makes the whole test glitch'''

mouse_function()