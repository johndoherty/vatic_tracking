from base import Path
import cv2

TRACKING_INTERVAL = 10

def filterboxes(path):
    frames = path.boxes.keys()
    maxframe = max(frames)
    keepframes = [frame for frame in frames
        if frame % TRACKING_INTERVAL == 0 or frame == maxframe]

    return Path(
        path.label,
        path.id,
        {frame: path.boxes[frame] for frame in keepframes}
    )

