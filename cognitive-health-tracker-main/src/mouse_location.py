import csv
import pandas as pd
import os
import sys
from datetime import datetime
import pyautogui

def mouse_location():
    mousedata = [datetime.now().strftime("%H_%M_%S"),pyautogui.position()]
    a=datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + ".csv"
    pd.read_csv(os.path.join(sys.path[0], "heatMap", a ))
    with open( a, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(mousedata)

mouse_location()