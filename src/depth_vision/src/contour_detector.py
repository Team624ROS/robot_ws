import cv2
import numpy as np
import math
from shape_detection import DetectShape

class ContourDetect:

    def __init__(self):
        self.detect_shape = DetectShape()
        self.last_x = 0
        self.last_y = 0

        # Change to change dynamicly
        self.x_threshhold = 100
        self.y_threshhold = 100

        # Change if camera is not in line with shooter
        self.camera_offset = 0

        self.lock_target = False

# Create class and get biggest contour with area if it does not detect contour use the last biggest contour and after 5 seconds of no reappearance got to the next biggest size. hanndle exemption when there is no contours
    def contour_detect(self, mask, is_tracking):

        if (is_tracking):
            edges = cv2.Canny(mask, 100, 150, apertureSize=3)

            _, contours, _= cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Where we eliminate some of the noise
            contour_list = []

            for contour in contours:
                area = cv2.contourArea(contour)
                perimeter = cv2.arcLength(contour,True)

                if (self.detect_shape.detect(contour, perimeter)):
                    contour_list.append(contour)

            if (len(contour_list) >= 1):
                biggest_contour = contour[0]
                target_contour = False
                for contour in contour_list:
                    (x,y,w,h) = cv2.boundingRect(contour)
                    
                    if (self.lock_target):
                        if (x < self.last_x + self.x_threshhold and x > self.last_x - self.x_threshhold):
                            if (y < self.last_y + self.y_threshhold and y > self.last_y - self.y_threshhold):
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

                cv2.circle(mask, (self.get_center(x, y-h, x + w, y + h).x, self.get_center(x, y-h, x + w, y + h).y), 2, (255, 0, 0))

                self.get_x_offset(self.get_center(x, y-h, x + w, y + h).x)
                self.get_y_offset(self.get_center(x, y-h, x + w, y + h).y)

                self.last_x = x
                self.last_y = y
            else:
                self.lock_target = False

        else:
            self.lock_target = False

        cv2.imshow('Contour image',mask)

    def get_center(self, x, y, w, h):
        return Point(x + (w/2), y + (h/2))

    def get_x_offset(self, x):
        pass

    def get_y_offset(self, y):
        pass


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


