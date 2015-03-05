#include "trackingmodule.h"

using namespace std;
using namespace cv;


string getImagePath(string basePath, int i) {
    stringstream ss;
    int folder1 = i / 100;
    int folder2 = i / 10000;
    ss << basePath << "/" << folder2 << "/" << folder1 << "/" << i << ".jpg"; 
    return ss.str();
}


void alltracks(int start, int stop, string basePath, vector<Rect> &boxes)
{

}

void singletrack(int start, int stop, string basePath, Rect initialBox, vector<Rect> &boxes)
{
    CompressiveTracker ct;
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

/*
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
