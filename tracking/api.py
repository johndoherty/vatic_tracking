import pytrack
import cpptrack
from utils import filterboxes
from tracking.base import Path


onlinetrackers = {}
onlinetrackers.update(pytrack.online)
onlinetrackers.update(cpptrack.online)

bidirectionaltrackers = {}
bidirectionaltrackers.update(pytrack.bidirectional)
bidirectionaltrackers.update(cpptrack.bidirectional)

multiobjecttrackers = {}
multiobjecttrackers.update(pytrack.multiobject)
multiobjecttrackers.update(cpptrack.multiobject)

def gettrackers():
    return {
        "online": onlinetrackers.keys(),
        "bidirectional": bidirectionaltrackers.keys(),
        "multiobject": multiobjecttrackers.keys()
    }

def online(tracker, start, stop, basepath, pathid, paths):
    if pathid not in paths:
        return Path(None, None, {})

    if start not in paths[pathid].boxes:
        return Path(path.label, path.id, {})

    if tracker in onlinetrackers:
        tracker = onlinetrackers[tracker]()
        return tracker.track(pathid, start, stop, basepath, paths)
    return None

def multiobject(tracker, start, stop, basepath, initialrect, paths):
    if tracker in multiobjecttrackers:
        return multiobjecttrackers[tracker].track(tracker, start, stop, basepath, paths)
    return None

def bidirectional(tracker, start, stop, basepath, pathid, paths):
    if pathid not in paths:
        return Path(None, None, {})

    if start not in paths[pathid].boxes or stop not in paths[pathid].boxes:
        return Path(path.label, path.id, {})

    if tracker in bidirectionaltrackers:
        tracker = bidirectionaltrackers[tracker]()
        return tracker.track(pathid, start, stop, basepath, paths)
    return None

