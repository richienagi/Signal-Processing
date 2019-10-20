# -*- coding: utf-8 -*-
"""
Please place the haarcascade_frontalface_default.xml file in the same directory as the face detect.py file.
https://github.com/opencv/opencv/tree/master/data/haarcascades
"""
import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
video = cv2.VideoCapture(0) #Start video captue from webcam

while True:
    loop_condition, frame = video.read()
    
    faces = face_cascade.detectMultiScale(frame, 1.1, 3)
    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
    cv2.imshow("Capturing",frame) 
    key = cv2.waitKey(1) #Press Escape key to stop while loop
    if key == 27:
        break

video.release() #Stop video acquistion from webcam
cv2.destroyAllWindows()


