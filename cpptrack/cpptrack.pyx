from tracking.base import Online, Bidirectional, MultiObject
from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp.map cimport map
from cython.operator cimport dereference as deref

TRACKING_INTERVAL = 10

cdef extern from "opencv2/opencv.hpp" namespace "cv":
    cdef cppclass Rect:
        Rect()
        Rect(int, int, int, int)
        int x, y, width, height

cdef extern from "trackingmodule.h":
    cdef cppclass Track:
        int start, stop
        vector[Rect] boxes
        string label

    cdef void compressivetrack(Rect initialBox, string basepath,
        int start, int stop, vector[Rect] boxes)

    cdef void bidirectionaltrack(initialBox, Rect finalBox, string basePath,
        int start, int stop, vector[Rect] boxes)

    cdef void alltracks(int start, int stop, string basePath,
        vector[vector[Rect]] boxes)

cdef boxestorects(vector[Rect] boxes):
    ret = []
    for i in range(0, boxes.size()-1, TRACKING_INTERVAL):
        outrect = {
            'rect':(boxes[i].x, boxes[i].y, boxes[i].width, boxes[i].height),
            'frame':i,
            'generated':(i!=0)
        }
        ret.append(outrect)

    lastframe = boxes.size() - 1
    lastrect = {
        'rect':(
            boxes[lastframe].x,
            boxes[lastframe].y,
            boxes[lastframe].width,
            boxes[lastframe].height
        ),
        'frame':lastframe,
        'generated':True,
    }
    ret.append(lastrect)
    return ret

cdef pyrecttorect(pyrect, Rect& r):
    r.x = int(pyrect[0])
    r.y = int(pyrect[1])
    r.width = int(pyrect[2])
    r.height = int(pyrect[3])

class Compressive(Online):
    def track(self, pathid, int start, int stop, initialrect, string basepath, paths):
        cdef vector[Rect] boxes
        cdef Rect r
        pyrecttorect(initialrect, r)
        compressivetrack(r, basepath, start, stop, boxes)
        return boxestorects(boxes)

online = {
    "Compressive": Compressive,
}

bidirectional = {}
multiobject = {}



"""
class CppTracking(Tracking):
    def __init__(self):
        cdef vector[string] v

        getForwardTrackerKeys(v)
        self.onlinetrackers = []
        for i in range(v.size()):
            self.onlinetrackers.append(v[i])

        getBidirectionalTrackerKeys(v)
        self.bidirectionaltrackers = []
        for i in range(v.size()):
            self.bidirectionaltrackers.append(v[i])

        getFullTrackerKeys(v);
        self.multiobjecttrackers = []
        for i in range(v.size()):
            self.multiobjecttrackers.append(v[i])

    def multiobject(self, string tracker, start, stop, string basepath):
        cdef vector[Track] tracks
        cdef FullTracker *t = fulltrackers[tracker]
        cdef int startframe = int(start)
        cdef int stopframe = int(stop)
        t.alltracks(startframe, stopframe, basepath, tracks)
        ret = []
        for i in range(tracks.size()):
            ret.append(tracktorects(tracks[i]))
        return ret

    def bidirectional(self, string tracker, string label,
            start, stop, string basepath, initialrect, finalrect):
        cdef int startframe = int(start)
        cdef int stopframe = int(stop)
        cdef int initialx = int(initialrect[0])
        cdef int initialy = int(initialrect[1])
        cdef int initialwidth = int(initialrect[2])
        cdef int initialheight = int(initialrect[3])
        cdef int finalx = int(finalrect[0])
        cdef int finaly = int(finalrect[1])
        cdef int finalwidth = int(finalrect[2])
        cdef int finalheight = int(finalrect[3])
        cdef Rect *initialr = new Rect(initialx, initialy, initialwidth, initialheight)
        cdef Rect *finalr = new Rect(finalx, finaly, finalwidth, finalheight)
        cdef BidirectionalTracker *t = bidirectionaltrackers[tracker]
        cdef Track track
        track.start = startframe
        track.stop = stopframe
        track.label = label
        t.bidirectionaltrack(deref(initialr), deref(finalr), basepath, track)
        return tracktorects(track)

    def online(self, string tracker, string label,
            start, stop, string basepath, initialrect):
        cdef int startframe = int(start)
        cdef int stopframe = int(stop)
        cdef int x = int(initialrect[0])
        cdef int y = int(initialrect[1])
        cdef int width = int(initialrect[2])
        cdef int height = int(initialrect[3])
        cdef Rect *r = new Rect(x, y, width, height)
        cdef ForwardTracker *t = forwardtrackers[tracker]
        cdef Track track
        track.start = startframe
        track.stop = stopframe
        track.label = label
        t.singletrack(deref(r), basepath, track)
        return tracktorects(track)

"""
