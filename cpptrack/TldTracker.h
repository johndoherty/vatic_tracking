/************************************************************************
* File:	CompressiveTracker.h
* Brief: C++ demo for paper: Kaihua Zhang, Lei Zhang, Ming-Hsuan Yang,"Real-Time Compressive Tracking," ECCV 2012.
* Version: 1.0
* Author: Yang Xian
* Email: yang_xian521@163.com
* Date:	2012/08/03
* History:
* Revised by Kaihua Zhang on 14/8/2012, 23/8/2012
* Email: zhkhua@gmail.com
* Homepage: http://www4.comp.polyu.edu.hk/~cskhzhang/
* Project Website: http://www4.comp.polyu.edu.hk/~cslzhang/CT/CT.htm
************************************************************************/
#ifndef _TLDTRACKER_H
#define _TLDTRACKER_H//一般是文件名的大写 头文件结尾写上一行：

#pragma once
#include "opencv2/opencv.hpp"
#include <vector>
#include "TLD.h"

using std::vector;
using namespace cv;
//---------------------------------------------------
class TldTracker
{
public:
	TldTracker(void);
	~TldTracker(void);

private:
	Mat last_gray;
	Mat current_gray;
	BoundingBox pbox;
	vector<Point2f> pts1;
	vector<Point2f> pts2;
  	bool status;
  	bool tl;

public:
	//TLD framework
	TLD tld;

public:
	void init(Mat& _frame, Rect& _objectBox);
	void processFrame(Mat& _frame, Rect& _objectBox);
private:
	void adaptBox(Rect& _objectBox, int imgW, int imgH);
};


#endif