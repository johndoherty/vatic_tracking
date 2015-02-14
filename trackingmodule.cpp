#include "opencv2/opencv.hpp"
#include <iostream>
#include <fstream>
#include <sstream>
#include <stdio.h>
#include <string.h>
#include "CompressiveTracker.h"
#include <Python.h>

using namespace std;
using namespace cv;

static PyObject * runTracking(PyObject *self, PyObject *args) {
    char * directoryName;
    string imageBasePath = string(directoryName)
}


void readImageSequenceFiles(string imgBasePath, vector <string> &imgNames, int firstImage=0)
{
	imgNames.clear();
	Mat image=imread(imgBasePath+"0.jpg");
	for (int frameCount=0; image.data!=NULL; frameCount++)
    {
		stringstream ss;
		ss<<frameCount;
		waitKey();
		imgNames.push_back(imgBasePath+ss.str()+".jpg");
		stringstream ss1;
		ss1<<frameCount+1;
		image=imread(imgBasePath+ss1.str()+".jpg");
	}
}
