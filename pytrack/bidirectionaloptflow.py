import numpy as np
import cv2
from tracking.base import Online, Bidirectional
from utils import getframes
from tracking.base import Path
from optflowutil import getpoints, meanshift

class BidirectionalOptFlow(Bidirectional):

    def track(self, pathid, start, stop, basepath, paths):
        path = paths[pathid]

        if start not in path.boxes or stop not in path.boxes:
            return Path(path.label, path.id, {})

        startbox = path.boxes[start]
        stopbox = path.boxes[stop]
        initialrect = (startbox.xtl, startbox.ytl, startbox.xbr-startbox.xtl, startbox.ybr-startbox.ytl)
        finalrect = (stopbox.xtl, stopbox.ytl, stopbox.xbr-stopbox.xtl, stopbox.ybr-stopbox.ytl)
        frames = getframes(basepath, False)
        previmage = frames[start]
        imagesize = previmage.shape

        forwardpoints = getpoints(start, stop, frames, startbox)
        backwardpoints = getpoints(stop, start, frames, stopbox)

        rowtoframe = sorted(list(set(forwardpoints.keys()) & set(backwardpoints.keys())))
        forwardmean = np.array([np.mean(forwardpoints[frame], axis=0) for frame in rowtoframe])
        backwardmean = np.array([np.mean(backwardpoints[frame], axis=0) for frame in rowtoframe])
        meandiff = np.sum(np.square(forwardmean - backwardmean), axis=1)
        mergeframe = rowtoframe[np.argmin(meandiff)]

        print "Start frame", start
        print "end frame", stop
        print "Merge frame", mergeframe
 
        startboxes = meanshift(start, mergeframe - 5, forwardpoints, initialrect, imagesize)
        stopboxes = meanshift(stop, mergeframe + 5, backwardpoints, finalrect, imagesize)
        boxes = {}
        for row, frame in enumerate(rowtoframe):
            if frame <= mergeframe and frame in startboxes:
                boxes[frame] = startboxes[frame]
            elif frame > mergeframe and frame in stopboxes:
                boxes[frame] = stopboxes[frame]

        """
        frametorow = {frame: row for row, frame in enumerate(rowtoframe)}
        for i in range(start, stop):
            image = frames[i]

            #if i in forwardpoints:
                #for row in forwardpoints[i]:
                #    cv2.circle(image, tuple(row), 4, 0, 1)

            #if i in backwardpoints:
                #cv2.circle(image, tuple(backwardmean[frametorow[i],:]), 6, 255, 3)
                #for row in backwardpoints[i]:
                #    cv2.circle(image, tuple(row), 4, 255, 1)

            if i in frametorow:
                cv2.putText(image, str(meandiff[frametorow[i]]), (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2)
                cv2.putText(image, "Frame" + str(i), (0, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2)
                cv2.circle(image, tuple(forwardmean[frametorow[i],:]), 6, 0, 3)
                cv2.circle(image, tuple(backwardmean[frametorow[i],:]), 6, 255, 3)

            # Draw it on image
            if i in boxes:
                box = boxes[i]
                if i < mergeframe:
                    cv2.rectangle(image, (box.xtl,box.ytl), (box.xbr,box.ybr), 0,2)
                else:
                    cv2.rectangle(image, (box.xtl,box.ytl), (box.xbr,box.ybr), 255,2)

            cv2.imshow('Optical flow tracking', image)
            cv2.waitKey()
        """

        cv2.destroyAllWindows()
        return Path(path.label, path.id, boxes)
        #return Path(path.label, path.id, boxes)


