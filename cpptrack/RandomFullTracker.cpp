#include "trackingmodule.h"


void alltracks(int start, int stop, std::string basePath, 
    std::vector<std::vector<cv::Rect> > &boxes)
{
    std::vector<cv::Rect> testtrack1;
    std::vector<cv::Rect> testtrack2;
    boxes.push_back(testtrack1);
    boxes.push_back(testtrack2);
    for (int i = start; i < stop; i++) {
        cv::Rect a(20, 20, 100, 100);
        cv::Rect b(200, 100, 100, 100);
        boxes[0].push_back(a);
        boxes[1].push_back(b);
    }
}
