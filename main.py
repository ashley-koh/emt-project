import logging
import sys
from tkinter import Tk, messagebox
import eel
from camera import VideoCamera
import base64
import time
import os

@eel.expose
def retrieve_images():
  path = "./web/images"
  images = os.listdir(path)
  return images

def show_error(title, msg):
  root = Tk()
  root.withdraw() #hide main window
  messagebox.showerror(title, msg)
  root.destroy()

def gen(camera):
  while True:
    frame = camera.get_frame()
    yield frame

@eel.expose
def video_feed():
  y = gen(x)

  for each in y:
    # Convert bytes to base64 encoded str, as we can only pass json to frontend
    blob = base64.b64encode(each)
    blob = blob.decode("utf-8")
    eel.updateImageSrc(blob)()

@eel.expose
def save_last_frame():
  x.save_last_frame()

@eel.expose
def stop_video_feed():
  x.stop_capturing()

@eel.expose
def restart_video_feed():
  x.restart_capturing()

def start_app():
  try:
    start_html_page = 'index.html'
    eel.init('web')
    logging.info("App Started")

    eel.start('index.html', size=(1000, 700))

  except Exception as e:
    err_msg = 'Could not launch a local server'
    logging.error('{}\n{}'.format(err_msg, e.args))
    show_error(title='Failed to initialise server', msg=err_msg)
    logging.info('Closing App')
    sys.exit()

if __name__ == "__main__":
  x = VideoCamera()
  start_app()