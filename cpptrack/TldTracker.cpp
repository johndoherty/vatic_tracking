#include "opencv2/opencv.hpp"
#include "TldTracker.h"
#include <math.h>
#include <iostream>
#include "tld_utils.h"
#include <sstream>
#include <stdio.h>
#include <algorithm>    // std::min
using namespace cv;
using namespace std;

//------------------------------------------------
TldTracker::TldTracker(void)
{
	//Read parameters file
	FileStorage fs;
	fs.open("/usr/local/config/TLDparameters.yml", FileStorage::READ);
	tld.read(fs.getFirstTopLevelNode());
    fs.release();
}

TldTracker::~TldTracker(void)
{
}

void TldTracker::adaptBox(Rect& _objectBox, int imgW, int imgH)
{
    //Keep _objectBox in the image, and bigger than tld.min_win
    _objectBox.x = std::max(1, _objectBox.x);
    _objectBox.y = std::max(1, _objectBox.y);
    _objectBox.x = std::min(imgW-tld.min_win, _objectBox.x);
    _objectBox.y = std::min(imgH-tld.min_win, _objectBox.y);
    _objectBox.width = std::max(tld.min_win, _objectBox.width);
    _objectBox.height = std::max(tld.min_win, _objectBox.height);
    _objectBox.width = std::min(imgW-_objectBox.x, _objectBox.width);
    _objectBox.height = std::min(imgH-_objectBox.y, _objectBox.height);

}

void TldTracker::init(Mat& _frame, Rect& _objectBox)
{
	//TLD initialization
	adaptBox(_objectBox, _frame.cols, _frame.rows);//Keep pbox in the image, and bigger than tld.min_wins
	tld.init(_frame,_objectBox);
	_frame.copyTo(last_gray);
	status=true;
	tl = true;
}
void TldTracker::processFrame(Mat& _frame, Rect& _objectBox)
{
	_frame.copyTo(current_gray);
    //Process Frame
    // ofstream f1("/tmp/test.log", ios::app);
    // f1<<"TldTracker.cpp 1 "<<"x:"<<pbox.x<<" y:"<<pbox.y<<" w:"<<pbox.width<<" h:"<<pbox.height<<endl;
    // f1.close();

    tld.processFrame(last_gray,current_gray,pts1,pts2,pbox,status,tl);

    //Keep pbox in the image, and bigger than tld.min_win
	adaptBox(pbox, _frame.cols, _frame.rows);

    _objectBox.x = pbox.x;
    _objectBox.y = pbox.y;
    _objectBox.width = pbox.width;
    _objectBox.height = pbox.height;
    //swap points and images
    swap(last_gray,current_gray);
    pts1.clear();
    pts2.clear();
}