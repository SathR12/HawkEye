import cv2 as cv

def isCircle(contour):  
    approx = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True)
   
    (coord_x, coord_y), radius = cv.minEnclosingCircle(contour)
    center = (int(coord_x), int(coord_y))
   
    contour_area = cv.contourArea(contour)
    x, y, w, h = cv.boundingRect(contour)
    aspect_ratio = w/h
   
    if  1.1 >= contour_area / (radius**2 * 3.14) >= .6 and contour_area > 200 and len(approx) > 7:
            return True
    return False