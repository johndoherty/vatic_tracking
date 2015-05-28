import numpy as np
import cv2
from tracking.base import Online
from utils import getframes
from tracking.base import Path
from optflowutil import getpoints, meanshift


class OpticalFlow(Online):

    def track(self, pathid, start, stop, basepath, paths):
        if pathid not in paths:
            return Path(None, None, {})

        path = paths[pathid]

        if start not in path.boxes:
            return Path(path.label, path.id, {})

        startbox = path.boxes[start]
        initialrect = (startbox.xtl, startbox.ytl, startbox.xbr-startbox.xtl, startbox.ybr-startbox.ytl)
        frames = getframes(basepath, False)
        previmage = frames[start]
        imagesize = previmage.shape

        prevpoints = np.array([])

        points = getpoints(start, stop, frames, startbox)
        boxes = meanshift(start, stop, points, initialrect, imagesize)

        """
        for i in range(start, stop):
            image = frames[i]

            if i in points:
                #cv2.circle(image, tuple(forwardmean[i,:]), 6, 0, 3)
                for row in points[i]:
                    cv2.circle(image, tuple(row), 4, 0, 1)

            if i in boxes:
                box = boxes[i]
                cv2.rectangle(image, (box.xtl,box.ytl), (box.xbr,box.ybr), 255,2)

            cv2.imshow('Optical flow tracking', image)
            cv2.waitKey(40)
        """

        cv2.destroyAllWindows()
        return Path(path.label, path.id, boxes)
