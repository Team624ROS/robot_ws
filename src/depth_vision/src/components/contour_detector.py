import cv2
import numpy as np
import math
from shape_detection import DetectShape
cv2 = cv2.cv2

def contour_detect(frame,mask,angle_list,count_none,start_detect,count_running,frame_count):

    black_template = np.zeros((480, 640, 3), dtype = "uint8")
    black_corner = np.zeros((480, 640, 3), dtype = "uint8")

    contours,_ = cv2.findContours(mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    contours_active = {}
    center_contour = {}
    center_contour_y = []
    angle_pair = []
    

    for contour in contours:

        area = cv2.contourArea(contour)
        if area > 175 :
            rows,cols = frame.shape[:2]
            vx,vy,x,y = cv2.fitLine(contour, cv2.DIST_L2,0,0.01,0.01)
            lefty = int((-x*vy/vx) + y)
            righty = int(((cols-x)*vy/vx)+y)


            angle = math.atan2(lefty - righty, 0 - cols-1) * 180 / math.pi
            if angle < -90 and angle > -135 or angle < 135 and angle > 90:
                M = cv2.moments(contour)

                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                center_contour_y.append(cy)
                center_contour[cy] = cx



    for contour in contours:
    
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour,True)
        
        if area > 175 :

            perimeter = cv2.arcLength(contour,True)

            peri = perimeter
            approx = cv2.approxPolyDP(contour,0.04 * peri, True)



            x1,y1,w,h = cv2.boundingRect(contour)
            

            rows,cols = frame.shape[:2]
            vx,vy,x,y = cv2.fitLine(contour, cv2.DIST_L2,0,0.01,0.01)
            lefty = int((-x*vy/vx) + y)
            righty = int(((cols-x)*vy/vx)+y)


            angle = math.atan2(lefty - righty, 0 - cols-1) * 180 / math.pi

            if angle < -100 and angle > -125 or angle < 125 and angle > 100:

                M = cv2.moments(contour)

                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                center_y = cy

                for c in center_contour_y:
                    if center_y != c:
                        if center_y < c + 60 and center_y > c - 60:                
                
        
                            rect = cv2.rectangle(frame,(x1,y1),(x1+w,y1+h),(255,0,0),2)
                            cv2.drawContours(black_corner,approx,-1,(0,255,0),3)
                            cv2.drawContours(frame,contour,-1,(0,255,0),3)
                            cv2.drawContours(black_template,contour,-1,(255,255,255),3)
                            contours_active[angle] = contour

                            cv2.circle(frame,(cx,cy),5,(255,255,255),10)
                            cv2.circle(frame,(center_contour[c],c),5,(255,255,255),10)


                

                            if righty >= -5000 and righty <= 5000 and lefty >= -5000 and lefty <= 5000:
                                cv2.line(frame,(cols-1,righty),(0,lefty),(0,255,255),2)   

    cv2.imshow("Final Img",frame)

    frame_set = False
    
    if len(contours_active.keys()) == 2:


        for key in contours_active.keys():
            angle_pair.append(key)

            
            
        angle_list.insert(0,angle_pair)

        count_none = 0
        start_detect = True

        angles = angle_pair
        count_running += 1
        frame_set = frame_count 
        print(count_running)

        if count_running > 20:

            print(angles)
            return (angles,angle_list,start_detect,count_none,count_running)

    if len(contours_active.keys()) < 2 or len(contours_active.keys()) > 2:
        
        if start_detect == True:
            if count_none < 4:
                angles = angle_list[0]

                count_none += 1
                count_running +=1

                print(angles)
                

                return [angles,angle_list,start_detect,count_none,count_running]
            else:
                count_running = 0
    
    
    
    return [False,count_running,frame_set]