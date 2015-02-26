#include "opencv2/opencv.hpp"
#include <assert.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <stdio.h>
#include <string.h>
#include "CompressiveTracker.h"

void track(int start, int stop, string basePath, Rect initialBox, vector<Rect> &boxes);