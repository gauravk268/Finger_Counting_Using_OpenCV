# Finger_Detection_Using_OpenCV

This will help in detecting fingers in a frame with the help of OpenCV.

<body>Steps: 
   <ul>
    <li>Capture an image</li>
    <li>Convert it to HSV</li>
    <li>Seperate out hand and background</li>
    <li>Apply morphological operations</li>
    <li>Find contours, find the one with max. area i.e. maxContour</li>
    <li>Create bounding rectangle around the maxContour</li>
    <li>Find number of convexity defects</li>
    <li>Print number of finger by counting no. of convexity defects</li>
   </ul>
    </body>
