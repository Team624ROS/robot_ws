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

from color_filter import ColorFilter
from contour_detector import ContourDetect

class DepthVisionTracking:

  def __init__(self):
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("camera/color/image_raw",Image,self.callback)
    self.cf = ColorFilter()
    self.cd = ContourDetect()

    # Subscribe to ros topic to tell if it should track
    self.is_tracking = True

    # Subscribe to ros topic to see if user wants to turn off target_lock
    self.lock_target = True

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    #(rows,cols,channels) = cv_image.shape

    # Color Filter the Video Stream (For Green)
    mask = self.cf.color_filter(cv_image,[50, 125,125],[90, 255,255],"mask")
    
    #cv2.imshow('Image window', mask)
    #cv2.imshow('Image', cv_image)

    self.cd.contour_detect(mask.copy(), self.is_tracking, self.lock_target)

    # Used for turret PID
    angular_feedback = self.cd.get_angular_pid().feedback
    angular_setpoint = self.cd.get_angular_pid().setpoint

    # Get Distance
    

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