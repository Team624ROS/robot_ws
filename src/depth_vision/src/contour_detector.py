import cv2
import numpy as np
import math
from shape_detection import DetectShape

class ContourDetect:

    def __init__(self):
        self.detect_shape = DetectShape()
        self.last_x = 0
        self.last_y = 0

        # Change if camera is not in line with shooter
        self.camera_offset = 0

        # Do not change will update in script (Current offset from "center" of frame)

        # Feedback of PID
        self.x_offset = 0
        self.wanted_x = 0

        # Used for distance
        self.y_offset = 0

        # Change to change dynamicly
        self.x_threshold = 100
        self.y_threshold = 100

        # Will make it harder to loose the target to other reflective materials (Uses the x and y threshold)
        self.lock_target = False

    def contour_detect(self, mask, is_tracking, lock_target):

        height, width = mask.shape

        # Setpoint of PID
        self.wanted_x = width/2 + self.camera_offset

        # Checks if you wish to target lock (default true )
        user_lock_target = lock_target


        if (is_tracking):
            # Detects edges to make easier for contours
            edges = cv2.Canny(mask, 100, 150, apertureSize=3)

            # List of all raw contours includes noise
            _, contours, _= cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Where we eliminate some of the noise
            contour_list = []

            # Loops through all contours and filters them by shape
            for contour in contours:
                area = cv2.contourArea(contour)
                perimeter = cv2.arcLength(contour,True)

                # Filters by shape
                if (self.detect_shape.detect(contour, perimeter)):
                    contour_list.append(contour)

            if (len(contour_list) >= 1):
                biggest_contour = contour[0]
                target_contour = False

                # Loops through filtered list to filter more
                for contour in contour_list:
                    (x,y,w,h) = cv2.boundingRect(contour)
                    
                    # Checks if it is locked on target
                    if (self.lock_target and user_lock_target):
                        if (x < self.last_x + self.x_threshold and x > self.last_x - self.x_threshold):
                            if (y < self.last_y + self.y_threshold and y > self.last_y - self.y_threshold):
                                if (cv2.contourArea(contour) > cv2.contourArea(biggest_contour)):
                                    biggest_contour = contour
                                    target_contour = True

                    elif (cv2.contourArea(contour) > cv2.contourArea(biggest_contour)):
                        biggest_contour = contour
                        self.lock_target = True
                        target_contour = True

            if (len(contour_list) >= 1 and target_contour):
                (x,y,w,h) = cv2.boundingRect(biggest_contour)
                cv2.rectangle(mask, (x ,y - h), (x + w, y + h), (255, 0, 0), 2)

                cv2.circle(mask, (self.get_center(x, y+h,w, h).x, self.get_center(x, y-h, w, h).y), 10, (255, 0, 0))

                self.x_offset = self.get_x_offset(self.get_center(x, y-h, w, h).x, width)
                self.y_offset = self.get_y_offset(self.get_center(x, y-h, w, h).y, height)

                print(self.x_offset, self.y_offset)

                self.last_x = x
                self.last_y = y

            else:
                self.lock_target = False

        else:
            self.lock_target = False

        cv2.imshow('Contour image',mask)

    def get_center(self, x, y, w, h):
        return Point(x + (w/2), y + h)

    def get_x_offset(self, x, width):
        return x - (self.wanted_x)

    def get_y_offset(self, y, height):
        return y - (height/2)
    
    def get_angular_pid(self):
        return AngularPID(self.x_offset, self.wanted_x)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class AngularPID:
    def __init__(self, x_offset, wanted_x):
        self.feedback = x_offset
        self.setpoint = wanted_x

