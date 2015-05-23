import os
import cv2

def getframes(basepath, color=True):
    return Frames(basepath, color)

class Frames:
    def __init__(self, basepath, color=True):
        self.basepath = basepath
        self.color = color

    def __getitem__(self, k):
        flag = cv2.CV_LOAD_IMAGE_COLOR if self.color else cv2.CV_LOAD_IMAGE_GRAYSCALE
        return cv2.imread(self.getframepath(k), flag);

    def getframepath(self, frame):
        folder1 = frame / 100;
        folder2 = frame / 10000;
        path = os.path.join(self.basepath, str(folder2), str(folder1), str(frame) + ".jpg")
        return path

    def __len__(self):
        f = 1
        while True:
            if not os.path.exists(self.getframepath(f)):
                return f
            f += 1

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]
