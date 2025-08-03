import threading
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, DirCreatedEvent, FileCreatedEvent
import os
import requests
from flask import Flask, jsonify, request

# Configure these files
PATH = 'monitorDirectory'
FILE_TYPES = ['.jpeg', '.jpg', '.png']
API_ENDPOINT = 'http://127.0.0.1:8000/date'

app = Flask(__name__)

def extract_datetime(file_path):
  try:
    img = Image.open(file_path)
    exif_data = img.getexif()
    for tagid in exif_data:
      tag_name = TAGS.get(tagid, tagid)
      if tag_name == 'DateTime':
        date_value = exif_data.get(tagid)  # DateTime value
        date_raw = datetime.strptime(date_value, "%Y:%m:%d %H:%M:%S")  # Remove the time
        formatted_date = date_raw.strftime("%m-%d-%Y")  # Format the date

        img.close()
        os.remove(file_path)
        return formatted_date
    # If no DateTime found, close and delete file
    img.close()
    os.remove(file_path)
  except Exception as e:
    print(f"Error processing file {file_path}: {e}")
  return None

class FileDetector(FileSystemEventHandler):
  def on_created(self, event: DirCreatedEvent | FileCreatedEvent) -> None:
    print(f"Detected file: {event.src_path}")
    if event.src_path.lower().endswith(('.jpg', '.jpeg', '.png')):
      date_time = extract_datetime(event.src_path)
      if date_time is None:
        date_time = 'null'
      request = {"date" : date_time}
      try:
        response = requests.post(API_ENDPOINT, json=request)
      except Exception as e:
        print('Failed to call', e)

    else:
      os.remove(event.src_path)
      request = {"date" : "null"}
      try:
        response = requests.post(API_ENDPOINT, json=request)
      except Exception as e:
        print('Failed to call', e)

def start_observer():
  event_handler = FileDetector()
  observer = Observer()
  observer.schedule(event_handler, PATH, recursive=False)
  observer.start()
  try:
    while True:
      observer.join(1)
  except KeyboardInterrupt:
    observer.stop()
  observer.join()

@app.route('/date', methods=["POST"])
def receive_date():
    print('Returned: ', request.json)
    return request.json

def run_flask_and_observer():
  observer_thread = threading.Thread(target=start_observer, daemon=True)
  observer_thread.start()
  app.run(debug=True, port=8000, use_reloader=False)

if __name__ == "__main__":
  run_flask_and_observer()