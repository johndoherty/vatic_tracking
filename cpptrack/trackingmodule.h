#include "opencv2/opencv.hpp"
#include <assert.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <stdio.h>
#include <string.h>
#include <vector>
#include <map>

float boxdistance(cv::Rect box1, cv::Rect box2);

void getFrame(int frame, std::string basepath, cv::Mat& out, bool color=true);

void compressivetrack(cv::Rect initialBox, std::string basepath,
    int start, int stop, std::vector<cv::Rect> &boxes);

void bidirectionaltrack(cv::Rect initialBox, cv::Rect finalBox, std::string basePath,
    int start, int stop, std::vector<cv::Rect> &boxes);

void alltracks(int start, int stop, std::string basePath, 
    std::vector<std::vector<cv::Rect> > &boxes);

//----------------- TLD --------------------
void tldtrack(cv::Rect initialBox, std::string basepath,
    int start, int stop, std::vector<cv::Rect> &boxes);

void bitldtrack(cv::Rect initialBox, cv::Rect finalBox, std::string basePath,
    int start, int stop, std::vector<cv::Rect> &boxes);