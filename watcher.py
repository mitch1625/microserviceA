import requests
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, DirCreatedEvent, FileCreatedEvent

# Change this to the directory you want to be monitored
PATH = 'monitorDirectory'


class FileDetector(FileSystemEventHandler):
  print('Watching for files')
  def on_created(self, event: DirCreatedEvent | FileCreatedEvent) -> None:
    print(f"Detected file: {event.src_path}")
    if event.src_path.lower().endswith(('.jpg', '.jpeg', '.png')):
      directory = event.src_path
      endpoint = 'http://127.0.0.1:8000/date'
      content = {"date" : directory}
      try:
        result = requests.post(url=endpoint, json=content)
        print(result.json())
      except Exception as e:
        print(e)
      os.remove(event.src_path)
    else:
      print(f'Unexpected Input. Deleting {event.src_path}')
      os.remove(event.src_path)


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

if __name__ == "__main__":
  start_observer()
