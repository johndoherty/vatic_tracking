#include "trackingmodule.h"
#include "CompressiveTracker.h"


void CompressiveTrackerModule::singletrack(Rect initialBox, string basePath, Track &track)
{
    CompressiveTracker ct;
    Rect box = initialBox;
    Mat gray;
    getFrame(track.start, basePath, gray, false);
    std::cout << track.label << std::endl;

    ct.init(gray, box);
    track.boxes.push_back(box);
    for (int i=track.start+1; i <= track.stop; i++) {
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
