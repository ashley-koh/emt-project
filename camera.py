import cv2 as cv
import numpy as np
import os, os.path
import random as rng

class VideoCamera(object):

  def __init__(self):

    self.VIDEO_DEVICE = 1
    self.IMAGE_WIDTH = 1000
    self.IMAGE_HEIGHT = 720

    self.video = cv.VideoCapture(self.VIDEO_DEVICE)
    # self.video = cv.VideoCapture('video.mp4')

    self.video.set(3, self.IMAGE_WIDTH) # Adjusts Width
    self.video.set(4, self.IMAGE_HEIGHT) # Adjusts Height

    self.last_frame = np.zeros((self.IMAGE_HEIGHT, self.IMAGE_WIDTH, 3), np.uint8)

    self.active = True

  def __del__(self):
    self.video.release()

  def stop_capturing(self):
    self.active = False

  def restart_capturing(self):
    self.active = True

  def save_last_frame(self):
    number_of_files = len([img for img in os.listdir('./images') if img[:6] == 'image-'])
    filename = './images/image-{}.jpg'.format(number_of_files)

    cv.imwrite(filename, self.last_frame)

    return filename

  def get_frame(self):

    if self.active:
      success, frame = self.video.read()

      # MAIN OPENCV CODE

      # We are using Motion JPEG, but OpenCV defaults to capture raw images,
      # so we must encode it into JPEG in order to correctly display the
      # video stream.

      print(self.VIDEO_DEVICE)

      frame = cv.flip(frame, 1)

      
      gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
      gray = cv.blur(gray, (3, 3))
      threshold = 60

      # mask
      ret, mask = cv.threshold(gray, 10, 255, cv.THRESH_BINARY)
      mask = cv.GaussianBlur(mask, (5, 5), 100)

      # Detect edges using canny
      canny_output = cv.Canny(gray, threshold, threshold * 2)

      # find contours
      contours, hierarchy = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

      contours_length = len(contours)
      contours_poly = [None] * contours_length
      boundRect = [None] * contours_length
      centers = [None] * contours_length
      radius = [None] * contours_length
      for i, c in enumerate(contours):
        contours_poly[i] = cv.approxPolyDP(c, 3, True)
        boundRect[i] = cv.boundingRect(contours_poly[i])
        centers[i], radius[i] = cv.minEnclosingCircle(contours_poly[i])

      drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)      

      # Draw polygonal contours + bounding box
      for i in range(len(contours)):
        color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
        area = cv.contourArea(contours_poly[i])

        if area > 120:
          # draw contours
          cv.drawContours(drawing, contours_poly, i, color)
          # draw bounding box
          cv.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])),
                    (int(boundRect[i][0] + boundRect[i][2]), int(boundRect[i][1] + boundRect[i][3])), color, 2)
          # text
          drawing = cv.putText(drawing, str(area), (int(boundRect[i][0]), int(boundRect[i][1])),
                            cv.FONT_HERSHEY_PLAIN, 1, color, 1, cv.LINE_AA)


      self.last_frame = drawing



    ret, jpeg = cv.imencode('.jpg', self.last_frame)
    return jpeg.tobytes()

  # OPENCV FUNCITONS
  def color(img):
    # Convert image into hsv
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # defining the range of Yellow color
    yellow_lower = np.array([22, 60, 200], np.uint8)
    yellow_upper = np.array([60, 255, 255], np.uint8)

    # finding the range yellow colour in the image
    yellow = cv.inRange(hsv, yellow_lower, yellow_upper)

    # Morphological transformation, Dilation
    kernal = np.ones((5, 5), "uint8")
    yellow = cv.dilate(yellow, kernal)
    res = cv.bitwise_and(img, img, mask=yellow)

    # Tracking Colour (Yellow)
    contours, hierarchy = cv.findContours(yellow, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
      area = cv.contourArea(contour)
      if (area > 300):
        x, y, w, h = cv.boundingRect(contour)
        img = cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)