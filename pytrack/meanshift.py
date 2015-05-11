import numpy as np
import cv2
from tracking.base import Online
from utils import getframes

class MeanShift(Online):
    def track(self, pathid, start, stop, initialrect, basepath, paths):
        frames = getframes(basepath, True)
        frame = frames[start]

        # setup initial location of window
        c,r,w,h = initialrect
        rect = initialrect
 
        # set up the ROI for tracking
        roi = frame[r:r+h, c:c+w]
        hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
        roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0,180])
        cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
 
        # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
        term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

        for i in range(start, stop):
            frame = frames[i]
            if frame is None:
                break

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            dst = cv2.calcBackProject([hsv], [0], roi_hist, [0,180], 1)

            # apply meanshift to get the new location
            _, rect = cv2.meanShift(dst, rect, term_crit)

            # Draw it on image
            x,y,w,h = rect
            img2 = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
            cv2.imshow('img2',img2)

            k = cv2.waitKey(60) & 0xff
            if k == 27:
                break
            else:
                cv2.imwrite(chr(k)+".jpg",img2)


        cv2.destroyAllWindows()
