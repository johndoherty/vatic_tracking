#include "trackingmodule.h"

void RandomFullTracker::alltracks(int start, int stop, std::string basePath, std::vector<Track> &tracks)
{
    Track testtrack1;
    Track testtrack2;
    tracks.push_back(testtrack1);
    tracks.push_back(testtrack2);
    for (int i = start; i < stop; i++) {
        cv::Rect a(20, 20, 100, 100);
        cv::Rect b(200, 100, 100, 100);
        tracks[0].boxes.push_back(a);
        tracks[1].boxes.push_back(b);
    }
}
