"""
Color picker using OpenCV and webcam
"""

MOUSE_LEFT = 1

import cv2
import numpy as np
import os
import ximea
from ximea import xiapi

RED     = 0
GREEN   = 1
BLUE    = 2
YELLOW  = 3

quadrant = RED
bgr_red     = np.array([0, 0, 255])
bgr_green   = np.array([0, 255, 0])
bgr_blue    = np.array([255, 0, 0])
bgr_yellow  = np.array([0, 255, 255])
save = False


def nothing(x):
    pass

def bgr2hsv(bgr):
    return cv2.cvtColor(np.array([[bgr.astype(np.uint8)]]), cv2.COLOR_BGR2HSV)[0][0]

def hsv2bgr(hsv):
    return cv2.cvtColor(np.array([[hsv]]), cv2.COLOR_HSV2BGR)[0][0]

def mouse_callback_frame(event, x, y, flags, params):
    global quadrant
    global bgr_red
    global bgr_green
    global bgr_blue
    global bgr_yellow
    if event == MOUSE_LEFT:
        bgr = image[y, x, :]
        if quadrant == RED:
            bgr_red = bgr
        elif quadrant == GREEN:
            bgr_green = bgr
        elif quadrant == BLUE:
            bgr_blue = bgr
        elif quadrant == YELLOW:
            bgr_yellow = bgr

def mouse_callback_palette(event, x, y, flags, params):
    global quadrant
    global save
    if event == MOUSE_LEFT:
        if x >= 0 and x < 800 and y >= 800 and y < 1000:
            save = True
        if x >= 0 and x < 400 and y >= 0 and y < 400:
            quadrant = RED
        elif x >= 400 and x < 800 and y >= 0 and y < 400:
            quadrant = GREEN
        elif x >= 0 and x < 400 and y >= 400 and y < 800:
            quadrant = BLUE
        elif x >= 400 and x < 800 and y >= 400 and y < 800:
            quadrant = YELLOW


# Create a black image, a window
palette = np.ones((1000, 800, 3), np.uint8)
cv2.namedWindow('palette')
cv2.namedWindow('frame')

cv2.setMouseCallback('frame', mouse_callback_frame, None)
cv2.setMouseCallback('palette', mouse_callback_palette, None)

#cap = cv2.VideoCapture(0)
cam = xiapi.Camera()
cam.open_device()
cam.set_exposure(10000)
cam_img = xiapi.Image()
cam.set_imgdataformat('XI_RGB24')
cam.disable_auto_wb()
cam.start_acquisition()
image = None

while True:
    #ret, frame = cap.read()
    cam.get_image(cam_img)
    img_data = cam_img.get_image_data_numpy()
    image = np.copy(img_data)
    palette[0:400, 0:400] = bgr_red
    palette[0:400, 400:800] = bgr_green
    palette[400:800, 0:400] = bgr_blue
    palette[400:800, 400:800] = bgr_yellow

    if quadrant == RED:
        palette = cv2.rectangle(palette, (10, 10), (390, 390), [128, 128, 128], 19)
    elif quadrant == GREEN:
        palette = cv2.rectangle(palette, (410, 10), (790, 390), [128, 128, 128], 19)
    elif quadrant == BLUE:
        palette = cv2.rectangle(palette, (10, 410), (390, 790), [128, 128, 128], 19)
    elif quadrant == YELLOW:
        palette = cv2.rectangle(palette, (410, 410), (790, 790), [128, 128, 128], 19)
    palette = cv2.putText(palette, "R", (130 + 30, 260 - 100), cv2.FONT_HERSHEY_SIMPLEX, 3, [0, 0, 0], 30)
    palette = cv2.putText(palette, "G", (530 + 30, 260 - 100), cv2.FONT_HERSHEY_SIMPLEX, 3, [0, 0, 0], 30)
    palette = cv2.putText(palette, "B", (130 + 30, 660 - 100), cv2.FONT_HERSHEY_SIMPLEX, 3, [0, 0, 0], 30)
    palette = cv2.putText(palette, "Y", (540 + 30, 660 - 100), cv2.FONT_HERSHEY_SIMPLEX, 3, [0, 0, 0], 30)
    palette = cv2.putText(palette, "R", (130 + 30, 260 - 100), cv2.FONT_HERSHEY_SIMPLEX, 3, [255, 255, 255], 10)
    palette = cv2.putText(palette, "G", (530 + 30, 260 - 100), cv2.FONT_HERSHEY_SIMPLEX, 3, [255, 255, 255], 10)
    palette = cv2.putText(palette, "B", (130 + 30, 660 - 100), cv2.FONT_HERSHEY_SIMPLEX, 3, [255, 255, 255], 10)
    palette = cv2.putText(palette, "Y", (540 + 30, 660 - 100), cv2.FONT_HERSHEY_SIMPLEX, 3, [255, 255, 255], 10)
    palette = cv2.putText(palette, "BGR: " + str(bgr_red), (60, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, [0, 0, 0], 12)
    palette = cv2.putText(palette, "BGR: " + str(bgr_red), (60, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, [255, 255, 255], 4)
    palette = cv2.putText(palette, "BGR: " + str(bgr_green), (460, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, [0, 0, 0], 12)
    palette = cv2.putText(palette, "BGR: " + str(bgr_green), (460, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, [255, 255, 255], 4)
    palette = cv2.putText(palette, "BGR: " + str(bgr_blue), (60, 700), cv2.FONT_HERSHEY_SIMPLEX, 0.8, [0, 0, 0], 12)
    palette = cv2.putText(palette, "BGR: " + str(bgr_blue), (60, 700), cv2.FONT_HERSHEY_SIMPLEX, 0.8, [255, 255, 255], 4)
    palette = cv2.putText(palette, "BGR: " + str(bgr_yellow), (460, 700), cv2.FONT_HERSHEY_SIMPLEX, 0.8, [0, 0, 0], 12)
    palette = cv2.putText(palette, "BGR: " + str(bgr_yellow), (460, 700), cv2.FONT_HERSHEY_SIMPLEX, 0.8, [255, 255, 255], 4)
    palette = cv2.putText(palette, "HSV: " + str(bgr2hsv(bgr_red)), (60, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.8, [0, 0, 0], 12)
    palette = cv2.putText(palette, "HSV: " + str(bgr2hsv(bgr_red)), (60, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.8, [255, 255, 255], 4)
    palette = cv2.putText(palette, "HSV: " + str(bgr2hsv(bgr_green)), (460, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.8, [0, 0, 0], 12)
    palette = cv2.putText(palette, "HSV: " + str(bgr2hsv(bgr_green)), (460, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.8, [255, 255, 255], 4)
    palette = cv2.putText(palette, "HSV: " + str(bgr2hsv(bgr_blue)), (60, 650), cv2.FONT_HERSHEY_SIMPLEX, 0.8, [0, 0, 0], 12)
    palette = cv2.putText(palette, "HSV: " + str(bgr2hsv(bgr_blue)), (60, 650), cv2.FONT_HERSHEY_SIMPLEX, 0.8, [255, 255, 255], 4)
    palette = cv2.putText(palette, "HSV: " + str(bgr2hsv(bgr_yellow)), (460, 650), cv2.FONT_HERSHEY_SIMPLEX, 0.8, [0, 0, 0], 12)
    palette = cv2.putText(palette, "HSV: " + str(bgr2hsv(bgr_yellow)), (460, 650), cv2.FONT_HERSHEY_SIMPLEX, 0.8, [255, 255, 255], 4)
    palette = cv2.putText(palette, "SAVE", (250, 940), cv2.FONT_HERSHEY_SIMPLEX, 4, [255, 255, 255], 8)
    if save:
        try:
            current_dir = os.getcwd()
            file = open(current_dir + "/colors.config", 'w+')
            file.write("{} {} {}\n".format(bgr_red[0], bgr_red[1], bgr_red[2]))
            file.write("{} {} {}\n".format(bgr_green[0], bgr_green[1], bgr_green[2]))
            file.write("{} {} {}\n".format(bgr_blue[0], bgr_blue[1], bgr_blue[2]))
            file.write("{} {} {}\n".format(bgr_yellow[0], bgr_yellow[1], bgr_yellow[2]))
            print("Saving color calibration files to {}/colors.config".format(current_dir))
            file.close()
            file = open(current_dir + "/colors.config", 'r')
            for line in file:
                print(line)
            save = False
        except Exception as e:
            print(e)
    cv2.imshow('frame', img_data)
    cv2.imshow('palette', palette)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.stop_acquisition()
cv2.destroyAllWindows()
