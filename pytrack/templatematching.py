import numpy as np
import vision
import cv2
from utils import getframes
from tracking.base import Online, Bidirectional
from tracking.base import Path

PADDING = 3

def filterlost(boxes, imagesize):
    newboxes = {}
    frames = sorted(boxes.keys())
    for frame in frames:
        newboxes[frame] = boxes[frame]
        if (frame != frames[0] and 
            (newboxes[frame].xtl < PADDING or
             newboxes[frame].ytl < PADDING or
             newboxes[frame].xbr > (imagesize[1] - PADDING) or
             newboxes[frame].ybr > (imagesize[0] - PADDING))):
            print "Lost at frame {0}".format(frame)
            newboxes[frame].lost = True
            break

    return newboxes

def samplerects(initialrect, imagesize):
    samples = [initialrect,]
    x, y, w, h = initialrect
    offsetx = int(0.5 * w)
    offsety = int(0.5 * w)
    for cx in range(x, x + w, 1):
        for cy in range(y, y + h, 1):
            rect = (cx - offsetx, cy - offsety, w, h)
            if (rect[0] >= 0 and
                rect[1] >= 0 and
                rect[0] + w < imagesize[1] and
                rect[1] + h < imagesize[0]):
                samples.append(rect)
    return samples

def templatematch(start, stop, initialrect, frames):
    previmage = frames[start]
    prevrect = initialrect
    imagesize = previmage.shape
    boxes = {}
    it = 1 if stop >= start else -1
    for i in range(start, stop, it):
        image = frames[i]
        rectscores = []
        prevpatch = previmage[prevrect[1]:prevrect[1] + prevrect[3], prevrect[0]:prevrect[0] + prevrect[2]]
        samples = samplerects(prevrect, imagesize)
        for rect in samples:
            patch = image[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]]
            #score = np.sum(np.square(prevpatch - patch))
            #score = np.sum((prevpatch - patch))
            score = np.sum(np.absolute(prevpatch - patch))
            #score = np.sum(patch)
            rectscores.append((rect, score))

        best = min(rectscores, key=lambda a: a[1])
        prevrect = best[0]
        previmage = image.copy()

        boxes[i] = vision.Box(
            max(0, prevrect[0]),
            max(0, prevrect[1]),
            min(imagesize[1], prevrect[0] + prevrect[2]),
            min(imagesize[0], prevrect[1] + prevrect[3]),
            frame=i,
            generated=True
        )

    return boxes

class TemplateMatch(Online):
    def track(self, pathid, start, stop, basepath, paths):
        path = paths[pathid]

        if start not in path.boxes:
            return Path(path.label, path.id, {})

        print "Tracking from {0} to {1}".format(start, stop)
        startbox = path.boxes[start]
        initialrect = (startbox.xtl, startbox.ytl, startbox.xbr-startbox.xtl, startbox.ybr-startbox.ytl)
        frames = getframes(basepath, False)
        boxes = templatematch(start, stop, initialrect, frames)
        boxes = filterlost(boxes, frames[0].shape)

        """
        for i in range(start, stop):
            image = frames[i]

            if i in boxes:
                box = boxes[i]
                cv2.rectangle(image, (box.xtl,box.ytl), (box.xbr,box.ybr), 255,2)

            cv2.imshow('Template tracking', image)
            cv2.waitKey(100)
        """

        cv2.destroyAllWindows()
        return Path(path.label, path.id, boxes)

def mergescore(box1, box2):
    center1 = ((box1.xtl + box1.xbr) / 2, (box1.ytl + box1.ybr) / 2)
    center2 = ((box2.xtl + box2.xbr) / 2, (box2.ytl + box2.ybr) / 2)
    return (center1[0] - center2[0])**2 + (center1[1] - center2[1])**2

class BidirectionalTemplateMatch(Bidirectional):
    def track(self, pathid, start, stop, basepath, paths):
        if pathid not in paths:
            return Path(None, None, {})

        path = paths[pathid]

        if start not in path.boxes:
            return Path(path.label, path.id, {})

        startbox = path.boxes[start]
        stopbox = path.boxes[stop]
        initialrect = (startbox.xtl, startbox.ytl, startbox.xbr-startbox.xtl, startbox.ybr-startbox.ytl)
        finalrect = (stopbox.xtl, stopbox.ytl, stopbox.xbr-stopbox.xtl, stopbox.ybr-stopbox.ytl)

        frames = getframes(basepath, False)
        forwardboxes = templatematch(start, stop, initialrect, frames)
        backwardboxes = templatematch(stop, start, finalrect, frames)

        commonframes = list(set(forwardboxes.keys()) & set(backwardboxes.keys()))
        scores = [mergescore(forwardboxes[i], backwardboxes[i]) for i in commonframes]
        mergeframe = min(zip(commonframes, scores), key=lambda a: a[1])[0]

        boxes = {}
        for frame in range(start, stop):
            if frame <= mergeframe and frame in forwardboxes:
                boxes[frame] = forwardboxes[frame]
            elif frame > mergeframe and frame in backwardboxes:
                boxes[frame] = backwardboxes[frame]


        """
        for i in range(start, stop):
            image = frames[i]

            if i in forwardboxes:
                box = forwardboxes[i]
                cv2.rectangle(image, (box.xtl,box.ytl), (box.xbr,box.ybr), 0,2)

            if i in backwardboxes:
                box = backwardboxes[i]
                cv2.rectangle(image, (box.xtl,box.ytl), (box.xbr,box.ybr), 255,2)

            if i == mergeframe:
                cv2.putText(image, "Merge frame", (0, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2)

            if i in frametorow:
                cv2.putText(image, str(meandiff[frametorow[i]]), (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2)
                cv2.putText(image, "Frame" + str(i), (0, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2)
                cv2.circle(image, tuple(forwardmean[frametorow[i],:]), 6, 0, 3)
                cv2.circle(image, tuple(backwardmean[frametorow[i],:]), 6, 255, 3)

            cv2.imshow('Optical flow tracking', image)
            cv2.waitKey()
        """

        cv2.destroyAllWindows()
        return Path(path.label, path.id, boxes)


