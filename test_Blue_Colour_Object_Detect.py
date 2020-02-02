import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    
    #ret tells us whether the image captured is successful or not
    if(not ret):
        continue

    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

    #bitwise-AND mask and original image
    result = cv2.bitwise_and(frame, frame, mask=mask)

    #to show the processed image
    cv2.imshow('Live_Feed', frame)
    cv2.imshow('Mask_Image', mask)
    cv2.imshow('Result_Image', result)
    
    if cv2.waitKey(1) == 27:    #since 27 is the equivalent of escape key
        break

cap.release()
cv2.destroyAllWindows()