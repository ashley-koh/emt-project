
import cv2

# [capture]
capture = cv2.VideoCapture(0)

while True:
    ret, frame = capture.read()
    if frame is None:
        break
    x = 59

    #Code

    # [show]
    cv2.imshow('Frame', frame)

    keyboard = cv2.waitKey(0)
    if keyboard == 'q' or keyboard == 27:
        break