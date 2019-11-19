import cv2
import numpy as np
import os, os.path

VIDEO_DEVICE = 0
IMAGE_WIDTH = 1000
IMAGE_HEIGHT = 720

class VideoCamera(object):

  def __init__(self):

    self.video = cv2.VideoCapture(VIDEO_DEVICE)
    # self.video = cv2.VideoCapture('video.mp4')

    self.video.set(3, IMAGE_WIDTH) # Adjusts Width
    self.video.set(4, IMAGE_HEIGHT) # Adjusts Height

    self.last_frame = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH, 3), np.uint8)

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

    cv2.imwrite(filename, self.last_frame)

    return filename

  def get_frame(self):

    if self.active:
      success, image = self.video.read()

      # MAIN OPENCV CODE

      # We are using Motion JPEG, but OpenCV defaults to capture raw images,
      # so we must encode it into JPEG in order to correctly display the
      # video stream.

      image = cv2.flip(image, 1)

      self.last_frame = image

    ret, jpeg = cv2.imencode('.jpg', self.last_frame)
    return jpeg.tobytes()