# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 12:45:35 2023

@author: julian
"""

import serial
import time
import numpy as np
# set up the serial line
ser = serial.Serial('COM5', 9600)
time.sleep(2)
# Read and record the data
data =[]                       # empty list to store the data


x = input("Start Program? Y/N")

if x == 'Y' or 'y':
    n = 1

while n == 1:
    b = ser.readline()         # read a byte string
    string_n = b.decode()  # decode byte string into Unicode  
    string = string_n.rstrip().isdigit() # remove \n and \r
    print(string)
    flt = float(string)        # convert string to float
    print(flt)
    data.append(flt)           # add to the end of data list
    time.sleep(0.1)            # wait (sleep) 0.1 seconds
    if flt < 1.0:
        print("GSR disconnected")
        n = 0
    

ser.close()
# show the data

for line in data:
    print(line)

import matplotlib.pyplot as plt
# if using a Jupyter notebook include

plt.figure()
plt.plot(data)
plt.xlabel('Time (seconds)')
plt.ylabel('Voltage')
plt.title('GSR vs. Time')
plt.show()

np.savetxt('GSR_data.csv', data, delimiter=',')