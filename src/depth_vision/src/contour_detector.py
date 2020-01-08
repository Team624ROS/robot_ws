import cv2
import numpy as np
import math
from shape_detection import DetectShape

detect_shape = DetectShape()
# Create class and get biggest contour with area if it does not detect contour use the last biggest contour and after 5 seconds of no reappearance got to the next biggest size. hanndle exemption when there is no contours
def contour_detect(mask):
    edges = cv2.Canny(mask, 100, 150, apertureSize=3)

    _, contours, _= cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 

    for contour in contours:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour,True)
        if (detect_shape.detect(contour, perimeter)):
            (x,y,w,h) = cv2.boundingRect(contour)
            cv2.rectangle(mask, (x ,y - h), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow('Contour image',mask)