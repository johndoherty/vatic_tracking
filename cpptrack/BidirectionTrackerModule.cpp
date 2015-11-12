/* Simple Bidirectional tracking module to serve as reference
 * Basically runs Compressive tracking forwards and backwards and tries to merge tracks
 *
 */

#include "trackingmodule.h"
#include "CompressiveTracker.h"
#include <math.h>


void bidirectionaltrack(cv::Rect initialBox, cv::Rect finalBox,
    std::string basePath, int start, int stop, vector<cv::Rect> &boxes)
{
    int totalboxes = stop-start;
    if (totalboxes  == 0) return;
    CompressiveTracker forwardtracker, backwardtracker;
    vector<Rect> forwardboxes, backwardboxes;
    std::vector<Rect>::iterator backwardit;
    Rect forwardbox = initialBox;
    Rect backwardbox = finalBox;
    Mat forwardgray, backwardgray;
    getFrame(start, basePath, forwardgray, false);
    getFrame(stop, basePath, backwardgray, false);

    forwardtracker.init(forwardgray, forwardbox);
    backwardtracker.init(backwardgray, backwardbox);
    forwardboxes.push_back(forwardbox);
    backwardit = backwardboxes.begin();
    backwardboxes.insert(backwardit, backwardbox);
    for (int i=1; i < totalboxes; i++) {
        getFrame(start+i, basePath, forwardgray, false);
        getFrame(stop-i, basePath, backwardgray, false);
        forwardtracker.processFrame(forwardgray, forwardbox);
        backwardtracker.processFrame(backwardgray, backwardbox);
        forwardboxes.push_back(forwardbox);
        backwardit = backwardboxes.begin();
        backwardboxes.insert(backwardit, backwardbox);
        /*
        rectangle(backwardgray, backwardbox, Scalar(0));
        std::cout << backwardgray.size() << std::endl;
        std::stringstream ss;
        ss << "debug/" << i << ".jpg"; 
        std::string path = ss.str();
        std::cout << path << std::endl;
        if(imwrite(path, backwardgray)) {
            std::cout << "Write successful" << std::endl;
        } else {
            std::cout << "Write unsuccessful!!" << std::endl;
        }
        waitKey(10);
        // */
    }

    float mindistance = boxdistance(forwardboxes[0], backwardboxes[0]);
    int mergeframe = 0;
    for (int i=0; i < totalboxes; i++) {
        float dist = boxdistance(forwardboxes[i], backwardboxes[i]);
        if (dist < mindistance) {
            mindistance = dist;
            mergeframe = i;
        }
    }

    for (int i=0; i < totalboxes; i++) {
        if (i < mergeframe) {
            boxes.push_back(forwardboxes[i]);
        } else {
            boxes.push_back(backwardboxes[i]);
        }
    }
}
