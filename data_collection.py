# Author: Bowen Zhang
#xvfb-run python3 data_collection.py if you from remote

# Import packages
import os
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import sys
from time import sleep
import termios, tty

# Get how many files in the DIR
def get_file_num(DIR):
    return len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

# Detect the keyboard input
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
 
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# The folder that store the images
data_path = './dataset'

# Get the categories that the image belongs to
category = input('Please input the category of the item that you are collecting:\n')

# Record the index of the images
image_index = 0
if os.path.isdir(data_path + '/' + category):
    image_index = get_file_num(data_path + '/' + category)
else:
    os.mkdir(data_path + '/' + category)

# Set up camera constants
# MAX is 1280
IM_WIDTH = 640
IM_HEIGHT = 640

# Initialize frame rate calculation
frame_rate_calc = 1
freq = cv2.getTickFrequency()
font = cv2.FONT_HERSHEY_SIMPLEX

# Initialize Picamera and grab reference to the raw capture
camera = PiCamera()
camera.resolution = (IM_WIDTH,IM_HEIGHT)
camera.framerate = 5
rawCapture = PiRGBArray(camera, size=(IM_WIDTH,IM_HEIGHT))
rawCapture.truncate(0)

# Wait the camera set up
wait_time = 4
current_time = 0

try:
    for frame1 in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):        
        # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
        # i.e. a single-column array, where each item in the column has the pixel RGB value
        frame = frame1.array
        frame.setflags(write=1)
        
        # Show the image
        cv2.imshow('Live Video', frame)
        cv2.waitKey(25)
        
        # detect keyboard
        key = getch()
        if 'q' in key:
            break
        elif 's' in key:
            # Show in the command line
            print('Save', image_index, 'shape', frame.shape)

            # Make the label in the same order
            if image_index < 10:
                str_index = '0' + str(image_index)
            else:
                str_index = str(image_index)

            # Save the image
            filename = data_path + '/' + category + '/' + category + '_' + str_index +'.jpg'
            cv2.imwrite(filename, frame)
            image_index += 1

            # Show the image
            cv2.imshow('Last time image', frame)
            cv2.waitKey(1)
        elif 'r' in key:
            if image_index > 0:
                # Get the index of the image
                image_index -= 1
                if image_index < 10:
                    str_index = '0' + str(image_index)
                else:
                    str_index = str(image_index)

                # Generate the remove function
                command = 'rm ' + data_path + '/' + category + '/' + category + '_' + str_index +'.jpg'
                
                # Do the command
                os.system(command)

                # Print in terminal
                print('Delete: ', str(image_index))


        # Get new frames
        rawCapture.truncate(0)

    # quit 
    camera.close()
    cv2.destroyAllWindows()

except KeyboardInterrupt:
    camera.close()
    cv2.destroyAllWindows()

