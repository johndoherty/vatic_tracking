import numpy as np
import cv2
from tracking.base import Online
from utils import getframes
import vision
from tracking.base import Path

MAX_CORNERS = 50
CORNER_QUALITY = 0.1;
MIN_CORNER_DIST = 2;

PAD = 5

class OpticalFlow(Online):
    def track(self, pathid, start, stop, basepath, paths):

        path = paths[pathid]

        if start not in path.boxes:
            return Path(path.label, path.id, [])

        startbox = path.boxes[start]
        initialrect = (startbox.xtl, startbox.ytl, startbox.xbr-startbox.xtl, startbox.ybr-startbox.ytl)
        frames = getframes(basepath, False)
        previmage = frames[start]
        imagesize = previmage.shape

        prevpoints = np.array([])

        box = startbox
        boxes = {}

        mask = np.zeros(imagesize, np.uint8)
        minx = max(0, box.xtl - PAD)
        maxx = min(imagesize[1], box.xbr + PAD)
        miny = max(0, box.ytl - PAD)
        maxy = min(imagesize[0], box.ybr + PAD)
        mask[miny:maxy, minx:maxx] = 255

        prevpoints = cv2.goodFeaturesToTrack(previmage, MAX_CORNERS, CORNER_QUALITY, MIN_CORNER_DIST, prevpoints, mask)


        for i in range(start, stop):
            nextimage = frames[i]
            if nextimage is None:
                break

            nextpoints, status, err = cv2.calcOpticalFlowPyrLK(previmage, nextimage, prevpoints);
            prevmatched = prevpoints[status == 1]
            nextmatched = nextpoints[status == 1]
            minx = nextmatched[:, 0].min()
            maxx = nextmatched[:, 0].max()
            miny = nextmatched[:, 1].min()
            maxy = nextmatched[:, 1].max()
            padx = max(0, (initialrect[2] - (maxx - minx)) / 2)
            pady = max(0, (initialrect[3] - (maxy - miny)) / 2)

            minx = max(0, minx - padx)
            maxx = min(imagesize[1], maxx + padx)
            miny = max(0, miny - pady)
            maxy = min(imagesize[0], maxy + pady)
            box = vision.Box(
                minx,
                miny,
                maxx,
                maxy,
                frame=i,
                generated=True
            )
            transform = cv2.estimateRigidTransform(prevpoints, nextpoints, False);
            boxes[i] = box
            previmage = nextimage
            prevpoints = nextpoints

            # Draw it on image
            #x,y,w,h = rect
            #cv2.rectangle(nextimage, (box.xtl,box.ytl), (box.xbr,box.ybr), 255,2)
            #cv2.imshow('img2',nextimage)
            #cv2.waitKey(20)

        cv2.destroyAllWindows()
        return Path(path.label, path.id, boxes)
