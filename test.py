import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys

objImg = cv2.imread('./images/ice-cream-stick.jpeg')
bgImg = cv2.imread('./images/background.jpeg')

try:
  # Init ORB Detector
  orb = cv2.ORB_create();


  objKP, objDES = orb.detectAndCompute( objImg, None )
  bgKP, bgDES = orb.detectAndCompute( bgImg, None )

  bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

  matches = bf.match(objDES, bgDES)

  matches = sorted(matches, key = lambda x:x.distance)

  finalImg = np.zeros(bgImg.shape, np.uint8)
  finalImg = cv2.drawMatches(objImg, objKP, bgImg, bgKP, matches[:500], finalImg, flags=2)

  plt.imshow(finalImg), plt.show()

except Exception as e:
  print(e)