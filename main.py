from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
from flask import Flask, jsonify, request

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
        return formatted_date
    img.close()
  except Exception as e:
    print(f"Error processing file {file_path}: {e}")
  return "null"

@app.route('/date', methods=["POST"])
def receive_date():
  print(request.json.get('date'))
  try:
    date_time = extract_datetime(request.json.get('date'))
    request.json['date'] = date_time
    print(request.json)
    return request.json
  except Exception as e:
    print(e)

if __name__ == "__main__":
  app.run(debug=True, port=8000, use_reloader=False)
