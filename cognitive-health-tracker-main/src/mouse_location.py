import csv
import pandas as pd
import os
import sys
from datetime import datetime

def mouse_location():
    mousedata = [datetime.now().strftime("%H_%M_%S"),pyautogui.position()]
    a=datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + ".csv"
    with open( a, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(mousedata)

mouse_location()