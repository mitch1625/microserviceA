from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, DirCreatedEvent, FileCreatedEvent
import os
import requests


# Configure these files
PATH = 'monitorDirectory'
FILE_TYPES = ['.jpeg', '.jpg', '.png']
API_ENDPOINT = 'http://127.0.0.1:8000/'

data = {}

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
    img.close()
  except Exception as e:
    print(f"Error processing file {file_path}: {e}")
  os.remove(file_path)
  return None

class FileDetector(FileSystemEventHandler):
  def on_created(self, event: DirCreatedEvent | FileCreatedEvent) -> None:

    if event.src_path.lower().endswith(('.jpg', '.jpeg', '.png')):
      print(f"Detected file: {event.src_path}")
      date_time = extract_datetime(event.src_path)


      if date_time is None:
        data['date'] = 'null'
      else:
        data['date'] = date_time

    else:
      os.remove(event.src_path)
      data['date'] = 'null'
    post_date(data['date'])

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


def post_date(date):
  payload = {"date": date}

  try:
    response = requests.post(API_ENDPOINT, json=payload)
    print(f"POST sent. Status Code: {response.status_code}, Response: {response.text}")
  except Exception as e:
      print(f"Failed to POST data: {e}")

if __name__ == "__main__":
    start_observer()
