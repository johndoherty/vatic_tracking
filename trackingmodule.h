#include "opencv2/opencv.hpp"
#include <assert.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <stdio.h>
#include <string.h>
#include <vector>
#include <map>

class Track {
public:
    int start;
    int stop;
    std::string label;
    std::vector<cv::Rect> boxes;
};

class Tracker {
public:
    Tracker() {};
    void getFrame(int frame, std::string basepath, cv::Mat& out, bool color=true);
};

class ForwardTracker: public Tracker {
public:
    ForwardTracker() {};
    virtual void singletrack(cv::Rect initialBox, std::string basePath, Track &track) = 0;
};

class BidirectionalTracker: public Tracker {
public:
    BidirectionalTracker() {};
    virtual void bidirectionaltrack(cv::Rect initialBox, cv::Rect finalBox, std::string basePath, Track &track) = 0;
};

class FullTracker: public Tracker {
public:
    FullTracker() {};
    virtual void alltracks(int start, int stop, std::string basePath, std::vector<Track> &tracks) = 0;
};

class CompressiveTrackerModule: public ForwardTracker {
public:
    CompressiveTrackerModule() {};
    void singletrack(cv::Rect initialBox, std::string basePath, Track &track);
};

class BidirectionalTrackerModule: public BidirectionalTracker {
private:
    float boxdistance(cv::Rect box1, cv::Rect box2);
public:
    BidirectionalTrackerModule() {};
    void bidirectionaltrack(cv::Rect initialBox, cv::Rect finalBox, std::string basePath, Track &track);
};

class RandomFullTracker: public FullTracker {
public:
    RandomFullTracker() {};
    void alltracks(int start, int stop, std::string basePath, std::vector<Track> &tracks);
};



void getForwardTrackers(std::map<std::string, ForwardTracker*> &trackers);
void getBidirectionalTrackers(std::map<std::string, BidirectionalTracker*> &trackers);
void getFullTrackers(std::map<std::string, FullTracker*> &trackers);

void getForwardTrackerKeys(std::vector<std::string> &keys);
void getBidirectionalTrackerKeys(std::vector<std::string> &keys);
void getFullTrackerKeys(std::vector<std::string> &keys);
