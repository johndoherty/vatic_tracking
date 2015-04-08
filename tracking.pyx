from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp.map cimport map
from cython.operator cimport dereference as deref

TRACKING_INTERVAL = 10

cdef extern from "opencv2/opencv.hpp" namespace "cv":
    cdef cppclass Rect:
        Rect(int, int, int, int)
        int x, y, width, height

cdef extern from "trackingmodule.h":
    cdef cppclass Track:
        int start, stop
        vector[Rect] boxes

    cdef cppclass ForwardTracker:
        void singletrack(int, int, Rect, string, Track)

    cdef cppclass BidirectionalTracker:
        void bidirectionaltrack(int, int, Rect, Rect, string, Track);

    cdef cppclass FullTracker:
        void alltracks(int, int, string, vector[Track])

    cdef void getForwardTrackers(map[string, ForwardTracker*])
    cdef void getBidirectionalTrackers(map[string, BidirectionalTracker*])
    cdef void getFullTrackers(map[string, FullTracker*])

    cdef void getForwardTrackerKeys(vector[string]);
    cdef void getBidirectionalTrackerKeys(vector[string]);
    cdef void getFullTrackerKeys(vector[string]);

cdef map[string, ForwardTracker*] forwardtrackers
cdef map[string, BidirectionalTracker*] bidirectionaltrackers
cdef map[string, FullTracker*] fulltrackers

getForwardTrackers(forwardtrackers)
getBidirectionalTrackers(bidirectionaltrackers)
getFullTrackers(fulltrackers)


cdef tracktorects(Track track):
    ret = []
    for i in range(0, track.boxes.size()-1, TRACKING_INTERVAL):
        outrect = {
            'rect':(track.boxes[i].x, track.boxes[i].y, track.boxes[i].width, track.boxes[i].height),
            'frame':i,
            'generated':(i!=0)
        }
        ret.append(outrect)

    lastframe = track.boxes.size() - 1
    lastrect = {
        'rect':(
            track.boxes[lastframe].x,
            track.boxes[lastframe].y,
            track.boxes[lastframe].width,
            track.boxes[lastframe].height
        ),
        'frame':lastframe,
        'generated':True,
    }
    ret.append(lastrect)
    return ret

def getforwardtrackers():
    cdef vector[string] v
    getForwardTrackerKeys(v)
    out = []
    for i in range(v.size()):
        out.append(v[i])
    return out

def getbidirectionaltrackers():
    cdef vector[string] v
    getBidirectionalTrackerKeys(v);
    out = []
    for i in range(v.size()):
        out.append(v[i])
    return out

def getfulltrackers():
    cdef vector[string] v
    getFullTrackerKeys(v);
    out = []
    for i in range(v.size()):
        out.append(v[i])
    return out

def runbidirectionaltracker(string tracker, start, stop, string basepath, initialrect, finalrect):
    cdef Track track
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
    print "Tracking from: {0} to {1}".format(start, stop)
    t.bidirectionaltrack(startframe, stopframe, deref(initialr), deref(finalr), basepath, track)
    return tracktorects(track)

def runforwardtracker(string tracker, start, stop, string basepath, initialrect):
    cdef Track track
    cdef int startframe = int(start)
    cdef int stopframe = int(stop)
    cdef int x = int(initialrect[0])
    cdef int y = int(initialrect[1])
    cdef int width = int(initialrect[2])
    cdef int height = int(initialrect[3])
    cdef Rect *r = new Rect(x, y, width, height)
    cdef ForwardTracker *t = forwardtrackers[tracker]
    print "Tracking from: {0} to {1}".format(start, stop)
    t.singletrack(startframe, stopframe, deref(r), basepath, track)
    return tracktorects(track)

#rects = run_tracking(67, 321, "/Users/john/Dropbox/School/JackRabbot/Jackrabbot/front_end/vatic/public/frames/video1", (150, 220, 40, 45))
#for rect in rects:
#    print rect
