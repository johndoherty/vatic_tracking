#include "trackingmodule.h"
#include "CompressiveTracker.h"

void compressivetrack(Rect initialBox, std::string basePath,
    int start, int stop, vector<Rect> &boxes)
{
    CompressiveTracker ct;
    Rect box = initialBox;
    Mat gray;
    getFrame(start, basePath, gray, false);
    //std::cout << label << std::endl;

    ct.init(gray, box);
    boxes.push_back(box);
    for (int i = start+1; i <= stop; i++) {
        getFrame(i, basePath, gray, false);
        ct.processFrame(gray, box);
        boxes.push_back(box);
        rectangle(gray, box, Scalar(0));
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
