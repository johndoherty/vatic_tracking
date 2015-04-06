#include "trackingmodule.h"
#include "CompressiveTracker.h"


void CompressiveTrackerModule::singletrack(int start, int stop, Rect initialBox, string basePath, Track &track)
{
    CompressiveTracker ct;
    Rect box = initialBox;
    Mat gray;
    getFrame(start, basePath, gray, false);

    ct.init(gray, box);
    track.boxes.push_back(box);
    for (int i=start+1; i <= stop; i++) {
        getFrame(i, basePath, gray, false);
        ct.processFrame(gray, box);
        track.boxes.push_back(box);
        /*rectangle(gray, box, Scalar(0));
        std::cout << gray.size() << std::endl;
        std::stringstream ss;
        ss << "debug/" << i << ".jpg"; 
        std::string path = ss.str();
        std::cout << path << std::endl;
        if(imwrite(path, gray)) {
            std::cout << "Write successful" << std::endl;
        } else {
            std::cout << "Write unsuccessful!!" << std::endl;
        }
        waitKey(10);*/
    }
}


