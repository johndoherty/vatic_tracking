import numpy as np
import vision
import cv2

def insideframe(rect, imagesize):
    return (rect[0] >= 0 and
            rect[1] >= 0 and
            rect[0] + rect[2] <= imagesize[1] and
            rect[1] + rect[3] <= imagesize[0])

def meanshift(start, stop, framepoints, initialrect, imagesize, iterations=5):
    boxes = {}
    rect = initialrect
    inc = 1 if start <= stop else -1
    for frame in range(start, stop, inc):
        if frame not in framepoints:
            continue
        haspoints = True
        rect = rectforpoints(framepoints[frame], rect, iterations)

        # If we updated the rect save it and continue to the next frame
        # otherwise mark as lost
        if haspoints and insideframe(rect, imagesize):
            boxes[frame] = vision.Box(
                max(0, rect[0]),
                max(0, rect[1]),
                min(imagesize[1], rect[0] + initialrect[2]),
                min(imagesize[0], rect[1] + initialrect[3]),
                frame=frame,
                generated=True
            )
        else:
            print "Frame {0} lost in {1} to {2}".format(frame, start, stop)
            boxes[frame] = vision.Box(
                max(0, rect[0]),
                max(0, rect[1]),
                min(imagesize[1], rect[0] + initialrect[2]),
                min(imagesize[0], rect[1] + initialrect[3]),
                frame=frame,
                lost=True,
                generated=True
            )
            break
    return boxes

def getmask(imagesize, box, pad=5):
    mask = np.zeros(imagesize, np.uint8)
    minx = max(0, box.xtl - pad)
    maxx = min(imagesize[1], box.xbr + pad)
    miny = max(0, box.ytl - pad)
    maxy = min(imagesize[0], box.ybr + pad)
    mask[miny:maxy, minx:maxx] = 255
    return mask

def rectforpoints(points, rect, iterations=5):
    for it in range(iterations):
        inwindow = np.empty((0,2))
        # Build a matrix of points in the search rect
        for point in points:
            if (rect[0] <= point[0] <= rect[0] + rect[2]
                and rect[1] <= point[1] <= rect[1] + rect[3]):
                inwindow = np.append(inwindow, [point], axis=0)

        # If no points in rect, we have lost the track
        if inwindow.shape[0] == 0:
            haspoints = False
            break

        # Center rect at mean of points in rect
        m = np.mean(np.array(inwindow), axis=0)
        rect = (m[0] - (0.5 * rect[2]), m[1] - (0.5 * rect[3]), rect[2], rect[3])
    return rect

def boxforpoints(points, width, height, imagesize, frame):
    m = np.mean(np.array(points), axis=0)
    rect = (m[0] - (0.5 * width), m[1] - (0.5 * height), width, height)
    rect = rectforpoints(points, rect)
    print imagesize
    print rect
    return vision.Box(
        max(0, rect[0]),
        max(0, rect[1]),
        min(imagesize[1], rect[0] + rect[2]),
        min(imagesize[0], rect[1] + rect[3]),
        frame=frame,
        generated=True
    )

def getpoints(start, stop, frames, firstbox, maxcorners=50, cornerquality=0.1, mincornerdist=2):
    result = {}
    firstrect = (firstbox.xtl, firstbox.ytl, firstbox.xbr-firstbox.xtl, firstbox.ybr-firstbox.ytl)
    previmage = frames[start]
    imagesize = previmage.shape

    prevpoints = np.array([])

    mask = getmask(imagesize, firstbox)
    prevpoints = cv2.goodFeaturesToTrack(previmage, maxcorners, cornerquality, mincornerdist, None, mask)
    prevpoints = np.reshape(prevpoints, (prevpoints.shape[0], 2))

    inc = 1 if start <= stop else -1
    for i in range(start, stop, inc):
        nextimage = frames[i]
        if nextimage is None:
            break
        
        result[i] = prevpoints
        #contrast = 1.2
        #maxvalue = 255 / 1.2
        #nextimage[nextimage > maxvalue] = maxvalue
        #nextimage *= contrast
        #nextimage[nextimage > 255] = 255

        nextpoints, status, err = cv2.calcOpticalFlowPyrLK(previmage, nextimage, prevpoints, None, None, None);
        status = np.reshape(status, (status.shape[0],))
        prevmatched = prevpoints[status == 1]
        nextmatched = nextpoints[status == 1]

        if nextmatched.shape[0] == 0:
            box = boxforpoints(prevpoints, firstrect[2], firstrect[3], imagesize, i)
            mask = getmask(imagesize, box)
            prevpoints = cv2.goodFeaturesToTrack(previmage, maxcorners, cornerquality, mincornerdist, None, mask)
            if prevpoints is None:
                result[i] = np.array([])
                break
            prevpoints = np.reshape(prevpoints, (prevpoints.shape[0], 2))
        else:
            prevpoints = nextmatched

        previmage = nextimage
    return result
