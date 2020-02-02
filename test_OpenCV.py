import cv2
import numpy as np

cap = cv2.VideoCapture(0)
while(1):                        #video loop
    ret, frame = cap.read()      #read the image
    cv2.imshow('image', frame)   #show the image
    if cv2.waitKey(1) == 27:     #27 is the ascii value for escape key, ends the video loop
        break

cv2.destroyAllWindow()
cv2.release()