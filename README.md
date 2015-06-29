VATIC Tracking Module
=====================

This is module provides a skeleton for tracking code that can be integrated with vatic.
It integrates with Python and C++, but it is meant to be easily extensible to other
languages.

There are three types of trackers:
- Forward trackers: For online tracking algorithms that take a single bounding box as
input from the first frame. It then uses this first bounding box to track to the last
frame.

- Bidirectional trackers: This is for tracking algorithms that take a bounding box in
the first and last frames as input and track between those two frames.

- Full trackers: These algorithms take no bounding boxes as input and perform detection
and tracking on an entire video.

