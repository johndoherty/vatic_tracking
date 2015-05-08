import pytrack
import cpptrack


onlinetrackers = {}
onlinetrackers.update(pytrack.online)
onlinetrackers.update(cpptrack.online)

bidirectionaltrackers = {}
bidirectionaltrackers.update(pytrack.bidirectional)
bidirectionaltrackers.update(cpptrack.bidirectional)

multiobjecttrackers = {}
multiobjecttrackers.update(pytrack.multiobject)
multiobjecttrackers.update(cpptrack.multiobject)

def online(tracker, label, start, stop, basepath, initialrect, pathid, paths):
    if tracker in onlinetrackers:
        paths = convertpaths(paths)
        return onlinetrackers[tracker].track(tracker, label, start, stop, basepath, initialrect)
    return None

def multiobject(tracker, start, stop, basepath, initialrect, paths):
    if tracker in multiobjecttrackers:
        paths = convertpaths(paths)
        return multiobjecttrackers[tracker].track(tracker, start, stop, basepath, paths)
    return None

def bidirectional(tracker, label, start, stop, basepath, initialrect, paths):
    if tracker in bidirectionaltrackers:
        paths = convertpaths(paths)
        return bidirectionaltrackers[tracker].track(tracker, label, start, stop, basepath, initialrect)
    return None

