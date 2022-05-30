#camera init.py

import cv2 as cv

class Camera:
    def __init__(self, cameo_source = 0):

        self.cam = cv.VideoCapture(cameo_source, cv.CAP_DSHOW)

        self.width = self.cam.get(cv.CAP_PROP_FRAME_WIDTH)
        self.height = self.cam.get(cv.CAP_PROP_FRAME_HEIGHT)

    def get_feed(self):
        if self.cam.isOpened():
            ret, frame = self.cam.read()
            if not ret is None :
                return ret, cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            
            else:
                return ret, None
        
    def __del__(self):
        if self.cam.isOpened():
            self.cam.release()


