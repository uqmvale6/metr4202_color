import cv2
import numpy as np
import os

RED     = 0
GREEN   = 1
BLUE    = 2
YELLOW  = 3

def bgr2hsv(bgr):
    return cv2.cvtColor(np.array([[bgr]]), cv2.COLOR_BGR2HSV)[0][0]

def hsv2bgr(hsv):
    return cv2.cvtColor(np.array([[hsv]]), cv2.COLOR_HSV2BGR)[0][0]

current_dir = os.getcwd()
file = open(current_dir + "/colors.config", 'r')
i = 0
bgr_red = None
bgr_green = None
bgr_blue = None
bgr_yellow = None
for line in file:
    entries = line.split(' ')[1:]
    values = [int(x) for x in entries]
    if i == RED:
        bgr_red = np.array([values[0], values[1], values[2]]).astype(np.uint8)
        hsv_red = bgr2hsv(bgr_red)
    if i == GREEN:
        bgr_green = np.array([values[0], values[1], values[2]]).astype(np.uint8)
        hsv_green = bgr2hsv(bgr_green)
    if i == BLUE:
        bgr_blue = np.array([values[0], values[1], values[2]]).astype(np.uint8)
        hsv_blue = bgr2hsv(bgr_blue)
    if i == YELLOW:
        bgr_yellow = np.array([values[0], values[1], values[2]]).astype(np.uint8)
        hsv_yellow = bgr2hsv(bgr_yellow)
    i += 1

print(bgr_red)
print(bgr_green)
print(bgr_blue)
print(bgr_yellow)

print(hsv_red)
print(hsv_green)
print(hsv_blue)
print(hsv_yellow)