from tracking.base import Online
from utils import getframes
from tracking.base import Path
import cv2

class BackgroundSubtract(Online):
    def track(self, pathid, start, stop, basepath, paths):
        bgs = cv2.BackgroundSubtractorMOG()
        frames = getframes(basepath, False)
        for frame in range(start, stop):
            fgmask = bgs.apply(frames[frame])

            cv2.imshow("Frame", fgmask)
            cv2.waitKey(40)
        cv2.destroyAllWindows()
        return Path(path.label, path.id, {})

