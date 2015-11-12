#include "trackingmodule.h"
#include "TldTracker.h"
#include <fstream>
#include <algorithm>    // std::min
using namespace std;

void tldtrack(Rect initialBox, string basePath,
    int start, int stop, vector<Rect> &boxes)
{
    TldTracker tldTracker;
    Rect box = initialBox;
    Mat gray;
    getFrame(start, basePath, gray, false);
    //std::cout << label << std::endl;

    tldTracker.init(gray, box);

    // ofstream f2("/tmp/test.log", ios::app);
    // f2<<"TldTrackerModule.cpp 2 "<<"x:"<<box.x<<" y:"<<box.y<<" w:"<<box.width<<" h:"<<box.height<<endl;
    // f2.close();

    boxes.push_back(box);
    //Added param
    stop = std::min(stop, start + tldTracker.tld.track_frame_num);
    for (int i = start+1; i <= stop; i++) {
        getFrame(i, basePath, gray, false);
        tldTracker.processFrame(gray, box);
        boxes.push_back(box);

        //rectangle(gray, box, Scalar(0));

        /*
        std::stringstream ss;
        ss << "debug/" << i << ".jpg"; 
        std::string path = ss.str();
        std::cout << path << std::endl;
        if(imwrite(path, gray)) {
            std::cout << "Write successful" << std::endl;
        } else {
            std::cout << "Write unsuccessful!!" << std::endl;
        }
        waitKey(10);
        */
    }
}
