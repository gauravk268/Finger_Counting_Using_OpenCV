import cv2
import numpy as np 

img = cv2.VideoCapture(0)

while(True):
    ret,image = img.read()

    if ret == 0:
        continue

    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, imageThresh = cv2.threshold(imageGray, 70, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(imageThresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    hull = [cv2.convexHull(c) for c in contours]

    imageFinal = cv2.drawContours(image.copy(), hull, -1, (255, 0, 0))

    cv2.imshow("Original", image)
    cv2.imshow("Threshold", imageThresh)
    cv2.imshow("Processed", imageFinal)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
img.release()