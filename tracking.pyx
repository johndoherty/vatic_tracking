from libcpp.string cimport string
from libcpp.vector cimport vector
from cython.operator cimport dereference as deref

cdef extern from "opencv2/opencv.hpp" namespace "cv":
    cdef cppclass Rect:
        Rect(int, int, int, int)
        int x, y, width, height

cdef extern from "trackingmodule.h":
    cdef void singletrack(int, int, string, Rect, vector[Rect])

def run_tracking(start, stop, string base_file_path, initial_rect):
    cdef vector[Rect] v
    cdef int start_frame = int(start)
    cdef int stop_frame = int(stop)
    cdef int x = int(initial_rect[0])
    cdef int y = int(initial_rect[1])
    cdef int width = int(initial_rect[2])
    cdef int height = int(initial_rect[3])
    cdef Rect *r = new Rect(x, y, width, height)
    singletrack(start_frame, stop_frame, base_file_path, deref(r), v)
    ret = []
    for i in range(0, v.size()-1, 5):
        out_rect_python = {'rect':(v[i].x, v[i].y, v[i].width, v[i].height), 'frame':i, 'generated':(i!=0)}
        ret.append(out_rect_python)
    last_frame = v.size() - 1
    last_rect = {
        'rect':(v[last_frame].x, v[last_frame].y, v[last_frame].width, v[last_frame].height),
        'frame':last_frame,
        'generated':False,
    }
    ret.append(last_rect)
    return ret

#rects = run_tracking(67, 321, "/Users/john/Dropbox/School/JackRabbot/Jackrabbot/front_end/vatic/public/frames/video1", (150, 220, 40, 45))
#for rect in rects:
#    print rect
