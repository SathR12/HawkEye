import cv2 as cv

def isSquare(contour):
    approx = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True)
    if len(approx) == 4 or len(approx) == 5:
        return True
    
    return False 