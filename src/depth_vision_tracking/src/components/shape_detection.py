import cv2
import numpy as np
cv2 = cv2.cv2

class DetectShape:

    def __init__(self):
        pass
    
    def detect(self,contour,perimeter):
        # get the shape name
        shape = "None"
        peri = perimeter
        approx = cv2.approxPolyDP(contour,0.04 * peri, True)
        print(len(approx))
        
        if len(approx) == 4:
            shape = "rectangle"


        return shape
