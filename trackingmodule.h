#include "opencv2/opencv.hpp"
#include <assert.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <stdio.h>
#include <string.h>
#include "CompressiveTracker.h"

void alltracks(int start, int stop, string basePath, vector<Rect> &boxes);
void singletrack(int start, int stop, string basePath, Rect initialBox, vector<Rect> &boxes);
void bidirectionaltrack(int start, int stop, string basePath,
        Rect initialBox, Rect finalBox, vector<Rect> &boxes);
