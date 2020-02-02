import cv2
import numpy as np 
import math

img = cv2.VideoCapture(0)

while(True):
    #captures image from the camera
    ret, image = img.read()

    #value of ret tells whether tha camera captured the image succesfully or not
    if  ret == 0:
        continue

    # Define range for the sub-window for the finger
    cv2.rectangle(image, (50, 50), (300, 300), (0, 255, 0), 0)
    image_crop = image[50:350, 50:350]

    # Apply Gaussian blur
    image_blur = cv2.GaussianBlur(image_crop, (3, 3), 0)

    # Change color-space from BGR to HSV
    image_hsv = cv2.cvtColor(image_blur, cv2.COLOR_BGR2HSV)

    # Create a binary image with where white will be skin colors and rest is black
    mask = cv2.inRange(image_hsv, np.array([0, 10, 60]), np.array([20, 150, 255]))

    # Kernel for morphological transformation
    kernel = np.ones((5, 5))

    # Apply morphological transformations to filter out the background noise
    image_dilation = cv2.dilate(mask, kernel, iterations=1)
    image_erosion = cv2.erode(image_dilation, kernel, iterations=1)

    # Apply Gaussian Blur and then Threshold
    image_filtered = cv2.GaussianBlur(image_erosion, (3, 3), 0)
    ret, image_thresh = cv2.threshold(image_filtered, 200, 255, 0)

    # Show threshold image
    cv2.imshow("Thresholded", image_thresh)

    # Find contours
    contours, hierarchy = cv2.findContours(image_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    drawing = np.zeros(image_crop.shape, np.uint8)
    try:
        # Find contour with maximum area
        contour = max(contours, key=lambda x: cv2.contourArea(x))

        # Create bounding rectangle around the contour
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image_crop, (x, y), (x + w, y + h), (0, 0, 255), 0)

        # Find convex hull
        hull = cv2.convexHull(contour)

        # Draw contour
        drawing = np.zeros(image_crop.shape, np.uint8)
        cv2.drawContours(drawing, [contour], -1, (0, 255, 0), 0)
        cv2.drawContours(drawing, [hull], -1, (0, 0, 255), 0)

        # Find convexity Print number of fingers number of fingerss
        hull = cv2.convexHull(contour, returnPoints=False)
        defects = cv2.convexityDefects(contour, hull)

        # Use cosine rule to find angle of the far point from the start and end point i.e. the convex points (the finger
        # tips) for all defects
        count_defects = 0

        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(contour[s][0])
            end = tuple(contour[e][0])
            far = tuple(contour[f][0])

            a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
            b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
            c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
            angle = (math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 180) / 3.14

            # if angle > 90 draw a circle at the far point
            if angle <= 90:
                count_defects += 1
                cv2.circle(image_crop, far, 1, [0, 0, 255], -1)

            cv2.line(image_crop, start, end, [0, 255, 0], 2)

        # Print number of fingers according to the number of convexity defects
        if count_defects == 0:
            cv2.putText(image, "ONE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255),5)
        elif count_defects == 1:
            cv2.putText(image, "TWO", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 5)
        elif count_defects == 2:
            cv2.putText(image, "THREE", (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 5)
        elif count_defects == 3:
            cv2.putText(image, "FOUR", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 5)
        elif count_defects == 4:
            cv2.putText(image, "FIVE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 5)
        else:
            pass
    except:
        pass

    # Show all the required images
    cv2.imshow("Gesture", image)
    all_image = np.hstack((drawing, image_crop))
    cv2.imshow('Contours', all_image)

    if cv2.waitKey(1) == 27:    #exits on escape
        break

cv2.destroyAllWindows()
img.release()