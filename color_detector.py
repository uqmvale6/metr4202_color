import cv2
import numpy as np
import os
from math import *
from numpy.core.fromnumeric import argmin
from ximea import xiapi

from color_picker import YELLOW
'''
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
'''

MOUSE_LEFT = 1
class ColorDetector:

    """
    Color detection class:
    Detects RGBY as well as White (W) and Black (K)
    """

    RED     = 0
    GREEN   = 1
    BLUE    = 2
    YELLOW  = 3
    WHITE   = 4
    BLACK   = 5

    def __init__(self, bgr_r, bgr_g, bgr_b, bgr_y):
        self.bgr_r = bgr_r
        self.bgr_g = bgr_g
        self.bgr_b = bgr_b
        self.bgr_y = bgr_y

        # Convert to hsv color space (H = Hue, S = Saturation, V = Value)
        self.hsv_r = ColorDetector.bgr2hsv(self.bgr_r)
        self.hsv_g = ColorDetector.bgr2hsv(self.bgr_g)
        self.hsv_b = ColorDetector.bgr2hsv(self.bgr_b)
        self.hsv_y = ColorDetector.bgr2hsv(self.bgr_y)

    @classmethod
    def bgr2hsv(cls, bgr):
        return cv2.cvtColor(np.array([[bgr]]), cv2.COLOR_BGR2HSV)[0][0]

    @classmethod
    def hsv2bgr(cls, hsv):
        return cv2.cvtColor(np.array([[hsv]]), cv2.COLOR_HSV2BGR)[0][0]

    @classmethod
    def hsv2coord(cls, hsv):
        """
        Maps to a cylinder with max radius = 1, height = 1
        This representation is singularity free compared to the HSV space
        """
        # Hue is normalised from 0 to 2 pi
        h = 2 * pi * hsv[0] / 180
        # Saturation is normalised from zero to 
        s = hsv[1] / 255
        v = hsv[2] / 255
        return np.array([s * v * cos(h), s * v * sin(h), v])

    def detect_color(self, bgr):
        """
        Color detection implementation
        Maps the HSV space as a cylinder, and finds the cartesian distance
        The closest distance color to the test color is the color returned.
        Black and white are also added to this color detection
        """
        hsv = ColorDetector.bgr2hsv(bgr)
        coord_test = ColorDetector.hsv2coord(hsv)
        coord_r = ColorDetector.hsv2coord(self.hsv_r)
        coord_g = ColorDetector.hsv2coord(self.hsv_g)
        coord_b = ColorDetector.hsv2coord(self.hsv_b)
        coord_y = ColorDetector.hsv2coord(self.hsv_y)
        coord_w = ColorDetector.hsv2coord(np.array([0, 0, 255]))
        coord_k = ColorDetector.hsv2coord(np.array([0, 0, 0]))
        
        dist_r = np.linalg.norm(coord_test - coord_r)
        dist_g = np.linalg.norm(coord_test - coord_g)
        dist_b = np.linalg.norm(coord_test - coord_b)
        dist_y = np.linalg.norm(coord_test - coord_y)
        dist_w = np.linalg.norm(coord_test - coord_w)
        dist_k = np.linalg.norm(coord_test - coord_k)

        return argmin([dist_r, dist_g, dist_b, dist_y, dist_w, dist_k])

def mouse_callback(event, x, y, flags, params):
    """
    Callback function when the image is left-clicked
    """
    image, color_detector = params
    if event == MOUSE_LEFT:
        bgr = image[y, x, :].astype(np.uint8)
        # Print out the color detected
        print("Detected " + ["red", "green", "blue", "yellow", "white", "black"][color_detector.detect_color(bgr)] + ".")



def demo():
    """
    This is demo code for color detection.
    You will need to modify this for your own implemention to use ROS.
    It is suggested to use a subscriber/publisher node to listen for Images, and publish the color detected.
    """
    # Read the colors.config file from each line and set the color arrays
    current_dir = os.getcwd()
    file = open(current_dir + "/colors.config", 'r')
    i = 0
    for line in file:
        entries = line.split(' ')
        values = [int(x) for x in entries]
        if i == 0:
            bgr_r = np.array([values[0], values[1], values[2]]).astype(np.uint8)
        if i == 1:
            bgr_g = np.array([values[0], values[1], values[2]]).astype(np.uint8)
        if i == 2:
            bgr_b = np.array([values[0], values[1], values[2]]).astype(np.uint8)
        if i == 3:
            bgr_y = np.array([values[0], values[1], values[2]]).astype(np.uint8)
        i += 1

    # Initialise the color detector
    color_detector = ColorDetector(bgr_r, bgr_g, bgr_b, bgr_y)

    # Setup the XIMEA Camera
    # For ROS, replace this with numpy array obtained from Image message
    cam = xiapi.Camera()
    cam.open_device()
    cam.set_exposure(10000)
    cam.set_imgdataformat('XI_RGB24')
    cam.disable_auto_wb()
    cam.start_acquisition()
    cam_img = xiapi.Image()
    
    # Setup image as empty numpy array
    image = np.zeros((cam.get_height(), cam.get_width(), 3), dtype=np.uint8)

    # Create a window named Image
    cv2.namedWindow('Image')
    cv2.setWindowTitle('Image', "XIMEA Camera View (press q to exit)")
    # Initialise the callback function
    cv2.setMouseCallback('Image', mouse_callback, (image, color_detector))

    # Main loop for image acquisition
    while True:
        try:
            cam.get_image(cam_img)
            img_data = cam_img.get_image_data_numpy()
            np.copyto(image, img_data)
            cv2.imshow("Image", image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except KeyboardInterrupt:
            break
    
    print("Stopping acquisition...")
    cam.stop_acquisition()
    print("Closing all windows...")
    cv2.destroyAllWindows()

if __name__ == "__main__":
    demo()
    