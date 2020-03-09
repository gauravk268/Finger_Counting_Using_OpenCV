# Finger_Detection_Using_OpenCV

This will help in detecting fingers in a frame with the help of OpenCV.

Steps: 
    *Capture an image
    *Convert it to HSV
    *Seperate out hand and background
    *Apply morphological operations
    *Find contours, find the one with max. area i.e. maxContour
    *Create bounding rectangle around the maxContour
    *Find number of convexity defects
    *Print number of finger by counting no. of convexity defects
