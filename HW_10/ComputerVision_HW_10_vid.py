# -*- coding: utf-8 -*-
"""CV_HomeWork_10.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Uxt0aQPAdoQJEFSp1qVHoHqp2UG5inqP
"""

import os
import cv2
import numpy as np
from time import time

# video data
data = "./data/test_video.MOV"

# Set up tracker
tracker_types = ['MIL','DaSiamRPN', 'GOTURN']
tracker_type = tracker_types[0]

if tracker_type == 'MIL':
    tracker = cv2.TrackerMIL_create()

if tracker_type == 'DaSiamRPN':
    tracker = cv2.TrackerDaSiamRPN_create()

if tracker_type == 'GOTURN':
    tracker = cv2.TrackerGOTURN_create()

color_types = ['color', 'grey']
color_type = color_types[0]

# Genrate tracking template
# Define a video capture object
vid = cv2.VideoCapture(data)
ret, frame = vid.read()
if ret:
    print("video is OK")
else:
    print("video isn't OK")

frame_width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
size = (frame_width, frame_height)
result = cv2.VideoWriter(f'./data/{tracker_type}_{color_type}.mp4', \
                         cv2.VideoWriter_fourcc(*'YUY2'), 30, size) # YUY2 - works, DIVX - doesn't work

# Initialize tracker
bbox = cv2.selectROI("output", frame, showCrosshair=True)

print(bbox)

ok = tracker.init(frame, bbox)

time1 = time()
while(True):
    ret, frame = vid.read()
    if ret:
        ok, bbox = tracker.update(frame)
        # Show the tracker working
        x1, y1 = bbox[0], bbox[1]
        width, height = bbox[2], bbox[3]
        if color_type == 'grey':
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x1+width), int(y1+height)), (0, 255, 0), 2)
        result.write(frame)
        #cv2.imshow('frame', frame)
    else:
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
##    if time() - time1 > 3:
##        break

cv2.destroyAllWindows()
vid.release()
result.release()
