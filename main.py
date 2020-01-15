import logging
import sys
from tkinter import Tk, messagebox
import eel
from camera import VideoCamera
import base64
import time
import os
import json

@eel.expose
def retrieve_images():
  path = "./web/images"
  images = os.listdir(path)
  return images[::-1]

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

@eel.expose
def select_frame(frame_number):
  x.select_frame(frame_number)

@eel.expose
def get_status():
  return x.status

@eel.expose
def get_colour():
  print(x.Color)
  colour = [int(x.Color[0]), int(x.Color[1]), int(x.Color[2])]
  return colour

@eel.expose
def get_data():

  with open('data.txt') as json_file:
    data = json.load(json_file)
    return data

@eel.expose
def update_config(configObj):
  x.maxWhite = configObj['maxWhite']
  x.brightness = configObj['brightness']
  x.threshold = configObj['threshold']
  x.size = configObj['size']
  x.dot = configObj['dot']
  x.noise = configObj['noise']

  add_new_config(configObj)

@eel.expose
def add_new_config(configObj):
  with open('data.txt') as json_file:
    data = json.load(json_file)
    data['config'].insert(0, configObj)
    with open('data.txt', 'w') as outfile:
      json.dump(data, outfile)

@eel.expose
def update_colour(colourObj):
  print(colourObj)
  with open('data.txt') as json_file:
    data = json.load(json_file)
    data['colour'] = {}
    data['colour'] = colourObj
    with open('data.txt', 'w') as outfile:
      json.dump(data, outfile)
  
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