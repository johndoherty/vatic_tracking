#ifndef _TLD_UTILS_H
#define _TLD_UTILS_H//一般是文件名的大写 头文件结尾写上一行：

#include <opencv2/opencv.hpp>
#pragma once



void drawBox(cv::Mat& image, CvRect box, cv::Scalar color = cvScalarAll(255), int thick=1); 

void drawPoints(cv::Mat& image, std::vector<cv::Point2f> points,cv::Scalar color=cv::Scalar::all(255));

cv::Mat createMask(const cv::Mat& image, CvRect box);

float median(std::vector<float> v);

std::vector<int> index_shuffle(int begin,int end);

#endif