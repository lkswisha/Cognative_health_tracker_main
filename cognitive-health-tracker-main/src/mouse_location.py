import csv
import pandas as pd
import os
import sys
from datetime import datetime

def mouse_location():
    print("Mouse location during Test")
    a=datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + ".csv"
    pd.read_csv(os.path.join(sys.path[0], "heatMap", a ))

mouse_location()