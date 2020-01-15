import cv2 as cv
import numpy as np
import os, os.path
import random as rng

class VideoCamera(object):

  def __init__(self):

    self.VIDEO_DEVICE = 0
    self.IMAGE_WIDTH = 1000
    self.IMAGE_HEIGHT = 720

    self.video = cv.VideoCapture(self.VIDEO_DEVICE)
    # self.video = cv.VideoCapture('video.mp4')

    self.video.set(3, self.IMAGE_WIDTH) # Adjusts Width
    self.video.set(4, self.IMAGE_HEIGHT) # Adjusts Height

    self.main_frame = np.zeros((self.IMAGE_HEIGHT, self.IMAGE_WIDTH, 3), np.uint8)
    self.masked_frame = np.zeros((self.IMAGE_HEIGHT, self.IMAGE_WIDTH, 3), np.uint8)
    self.gray_frame = np.zeros((self.IMAGE_HEIGHT, self.IMAGE_WIDTH, 3), np.uint8)
    self.last_frame = np.zeros((self.IMAGE_HEIGHT, self.IMAGE_WIDTH, 3), np.uint8)

    # 0 = main frame
    # 1 = masked frame
    # 2 = gray frame
    # 3 = last frame
    self.selected_frame = 3
    #Settings
    self.maxWhite = 450 #Threshold for white
    self.brightness = 5 #Increase in brightness
    self.threshold = 35 #Threshold for canny
    self.size = 14750 #Min size of stick
    self.dot = 300 #Max size of dot
    self.noise = 60 #Min size of dot

    #Outputs
    self.Color = [0, 0, 0] #Color of stick
    self.status = "Initializing"

    self.active = True

  def __del__(self):
    self.video.release()

  def stop_capturing(self):
    self.active = False

  def restart_capturing(self):
    self.active = True

  def save_last_frame(self):
    number_of_files = len([img for img in os.listdir('./web/images') if img[:6] == 'image-'])
    filename = './web/images/image-{}.jpg'.format(number_of_files)

    cv.imwrite(filename, self.last_frame)

    return filename

  def select_frame(self, frame_number):
    self.selected_frame = frame_number

  def color(self, img, k, Color, maxWhite):
    Z = img.reshape((-1, 3))

    # convert to np.float32
    Z = np.float32(Z)

    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 4, 0.75)
    ret, label, center = cv.kmeans(Z, k, None, criteria, 2, cv.KMEANS_RANDOM_CENTERS)

    for i in range (len(center)):
        col = center[i]
        num = col[0] + col[1] + col[2]
        if num < maxWhite:
            self.Color = center[i]

    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((img.shape))

    return res2

  def get_frame(self):

    if self.active:
      success, frame = self.video.read()

      # MAIN OPENCV CODE

      # We are using Motion JPEG, but OpenCV defaults to capture raw images,
      # so we must encode it into JPEG in order to correctly display the
      # video stream.

      frame = cv.flip(frame, 1)

      main = frame

      frame = increase_brightness(frame, self.brightness)
      frame = color(frame, 2, self.Color, self.maxWhite)

      gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

      # Detect edges using Canny
      canny_output = cv.Canny(gray, self.threshold, self.threshold * 2)

      # find contours
      contours, hierarchy = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

      contours_poly = [None] * len(contours)
      boundRect = [None] * len(contours)
      centers = [None] * len(contours)
      radius = [None] * len(contours)
      for i, c in enumerate(contours):
        contours_poly[i] = cv.approxPolyDP(c, 1, True)
        boundRect[i] = cv.boundingRect(contours_poly[i])
        centers[i], radius[i] = cv.minEnclosingCircle(contours_poly[i])

      drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)

      # Draw polygonal contour + bonding box

      status = "Nothing detected"
      for i in range(len(contours)):
        area = cv.contourArea(contours_poly[i])
        red = (255, 89, 100)
        yellow = (255, 231, 76)
        lightBlue = (53, 167, 255)

        #non broken stick
        if area > self.size and area < 39000:
          self.status = "Not Broken"
          # draw contours
          cv.drawContours(drawing, contours_poly, i, lightBlue)
          # draw bounding box
          cv.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])),
                (int(boundRect[i][0] + boundRect[i][2]), int(boundRect[i][1] + boundRect[i][3])), lightBlue, 2)
          drawing = cv.putText(drawing, "Not Broken", (int(boundRect[i][0]), int(boundRect[i][1])-13),
                            cv.FONT_HERSHEY_PLAIN, 1, lightBlue, 1, cv.LINE_AA)
          status = "Not broken"

          # area
          drawing = cv.putText(drawing, str(area), (int(boundRect[i][0]), int(boundRect[i][1])-2),
                            cv.FONT_HERSHEY_PLAIN, 1, lightBlue, 1, cv.LINE_AA)

        #broken stick
        elif area > self.dot and area < self.size:
          self.status = "Broken"
          # draw contours
          cv.drawContours(drawing, contours_poly, i, red)
          # draw bounding box
          cv.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])),
                    (int(boundRect[i][0] + boundRect[i][2]), int(boundRect[i][1] + boundRect[i][3])), red, 2)
          drawing = cv.putText(drawing, "Broken", (int(boundRect[i][0]), int(boundRect[i][1])-15),
                            cv.FONT_HERSHEY_PLAIN, 1, red, 1, cv.LINE_AA)
          status = "Broken"
          # area
          drawing = cv.putText(drawing, str(area), (int(boundRect[i][0]), (int(boundRect[i][1]))),
                            cv.FONT_HERSHEY_PLAIN, 1, red, 1, cv.LINE_AA)

        #dots
        if area > self.noise and area < self.dot:
          self.status = "Dots Present"
          # draw contours
          cv.drawContours(drawing, contours_poly, i, yellow)
          # draw bounding box
          cv.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])),
                    (int(boundRect[i][0] + boundRect[i][2]), int(boundRect[i][1] + boundRect[i][3])), yellow, 2)
          drawing = cv.putText(drawing, "Dot", (int(boundRect[i][0]), int(boundRect[i][1])),
                            cv.FONT_HERSHEY_PLAIN, 1, yellow, 1, cv.LINE_AA)
          # area
          #drawing = cv.putText(drawing, str(area), (int(boundRect[i][0]), (int(boundRect[i][1])) + 10),
                            #cv.FONT_HERSHEY_PLAIN, 1, yellow, 1, cv.LINE_AA)

      gray = cv.cvtColor(main, cv.COLOR_BGR2GRAY)



      self.main_frame = main
      self.masked_frame = frame
      self.gray_frame = gray
      # self.last_frame = drawing

      if self.selected_frame == 0:
        self.last_frame = main

      elif self.selected_frame == 1:
        self.last_frame = frame

      elif self.selected_frame == 2:
        self.last_frame = gray

      elif self.selected_frame == 3:
        self.last_frame = drawing
      

    ret, jpeg = cv.imencode('.jpg', self.last_frame)
    return jpeg.tobytes()

# OPENCV FUNCITONS
def increase_brightness(img, value):
  hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
  h, s, v = cv.split(hsv)

  lim = 255 - value
  v[v > lim] = 255
  v[v <= lim] += value

  final_hsv = cv.merge((h, s, v))
  img = cv.cvtColor(final_hsv, cv.COLOR_HSV2BGR)
  return img

def color(img, k, Color, maxWhite):
  Z = img.reshape((-1, 3))

  # convert to np.float32
  Z = np.float32(Z)

  # define criteria, number of clusters(K) and apply kmeans()
  criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 4, 0.75)
  ret, label, center = cv.kmeans(Z, k, None, criteria, 2, cv.KMEANS_RANDOM_CENTERS)

  for i in range (len(center)):
      col = center[i]
      num = col[0] + col[1] + col[2]
      if num < maxWhite:
          Color = center[i]

  center = np.uint8(center)
  res = center[label.flatten()]
  res2 = res.reshape((img.shape))

  return res2
