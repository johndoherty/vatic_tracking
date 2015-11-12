#include "trackingmodule.h"

using namespace std;
using namespace cv;

float boxdistance(Rect box1, Rect box2)
{
    return sqrt(pow((box1.x - box2.x), 2) +
        pow((box1.y - box2.y), 2));
}

void getFrame(int frame, string basePath, Mat& out, bool color) {
    Mat tmp;
    stringstream ss;
    int folder1 = frame / 100;
    int folder2 = frame / 10000;
    ss << basePath << "/" << folder2 << "/" << folder1 << "/" << frame << ".jpg"; 
    string path = ss.str();

    tmp = imread(path);
    tmp.copyTo(out);
    if (!color) {
        cvtColor(out, out, CV_RGB2GRAY);
    }
}


// This is where you initialize tracking algorithms
/*
void getForwardTrackers(map<string, ForwardTracker*> &trackers) {
    trackers.clear();
    trackers["Compressive"] = new CompressiveTrackerModule();
}

void getBidirectionalTrackers(map<string, BidirectionalTracker*> &trackers) {
    trackers.clear();
    trackers["Compressive-Bidirectional"] = new BidirectionalTrackerModule();
}

void getFullTrackers(map<string, FullTracker*> &trackers) {
    trackers.clear();
    trackers["RandomTestTracker"] = new RandomFullTracker();
}

template<typename T> void getKeyForMap(map<string, T> m, vector<string>& v) {
    v.clear();
    for(typename map<string, T>::iterator it = m.begin(); it != m.end(); ++it) {
        v.push_back(it->first);
    }
}

void getForwardTrackerKeys(vector<string> &keys) {
    map<string, ForwardTracker*> m;
    getForwardTrackers(m);
    getKeyForMap<ForwardTracker*>(m, keys);
}

void getBidirectionalTrackerKeys(vector<string> &keys) {
    map<string, BidirectionalTracker*> m;
    getBidirectionalTrackers(m);
    getKeyForMap<BidirectionalTracker*>(m, keys);
}

void getFullTrackerKeys(vector<string> &keys) {
    map<string, FullTracker*> m;
    getFullTrackers(m);
    getKeyForMap<FullTracker*>(m, keys);
}

void bidirectionaltrack(int start, int stop, string basePath,
        Rect initialBox, Rect finalBox, vector<Rect> &boxes)
{
    CompressiveTracker forwardct, backwardct;
    Rect box = initialBox;
    Mat image, gray;
    image = imread(getImagePath(basePath, start));
    cvtColor(image, gray, CV_RGB2GRAY);
    ct.init(gray, box);
    boxes.push_back(box);
    for (int i=start+1; i <= stop; i++) {
        image = imread(getImagePath(basePath, i));
        cvtColor(image, gray, CV_RGB2GRAY);
        ct.processFrame(gray, box);
        boxes.push_back(box);
        rectangle(image, box, Scalar(0, 0, 0), 2);
        waitKey(10);
    }
}
*/
