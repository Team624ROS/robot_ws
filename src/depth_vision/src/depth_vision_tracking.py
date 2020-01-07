#!/usr/bin/env python
from __future__ import print_function

import cv2
from matplotlib import pyplot as plt
import numpy as np
import roslib
import sys
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
#from components.color_filter import ColorFilter
#from components.contour_detector import contour_detect

class DepthVisionTracking:

  def __init__(self):
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("camera/color/image_raw",Image,self.callback)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    (rows,cols,channels) = cv_image.shape

    cv2.imshow("Image window", cv_image)
    cv2.waitKey(3)

def main(args):
  dvt = DepthVisionTracking()
  rospy.init_node('Depth Image ', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)

'''
cv2 = cv2.cv2

cf = ColorFilter()
# Initiate Camera
cap = cv2.VideoCapture(0)
frame_count = 1

frame_list = {}
angle_list = []
count_none = 0 
start_detect = False
count_running = 0

# Main loop
while True:
    # Get Frames from Camera
    ret,frame = cap.read()

    # Color Filter the Video Stream (For Blue)
    # Lower:[80,50,50] and Higher:[140,255,255] NEW = [80,70,60]and[115,255,190]
    hsv_frame = cf.color_filter(frame,[38,86,0],[121,255,230],"res")
    mask = cf.color_filter(frame,[30,86,0],[121,255,230],"mask")
    gray = cf.color_filter(frame,[38,86,0],[121,255,230],"gray")

    # detect and return stuff
    all_return = contour_detect(hsv_frame.copy(),mask,angle_list,count_none,start_detect,count_running,frame_count)

    if all_return[0] != False:
        angles = all_return[0]
        angle_list = all_return[1]
        start_detect = all_return[2]
        count_none = all_return[3]
        count_running = all_return[4]

    # Need to fix frame counting stuff
    else:
        count_running = all_return[1]
        frame_set = all_return[2]
        if frame_set == False:
            pass
        elif frame_count - frame_set > 150:
                count_running = 0
                

    



    

    # Count the num of frames that passed 
    frame_count += 1

    # Exit if "q" is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
'''