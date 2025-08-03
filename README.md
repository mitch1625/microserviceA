
# Image DateTime Extractor

This microservice receives an image in `.jpg`, `.jpeg`, or `.png` format and extracts the “Exif.Image.DateTime” from the exif metadata of the image. The information is returned as JSON.
If DateTime is present, `{'date' : 'MM-DD-YYYY}` is returned, where `MM-DD-YYYY` is the DateTime information extracted.


1. `watcher.py` continuously monitors a specified directory. Once a file is placed into that directory, that file is processed for Image.DateTime data. The data sent into the `POST` request is `{'data' : 'directory_being_monitored'}`, where `directory_being_monitored` is the directory being watched for files.

2. The input is analyzed and if `DateTime` is present it is extracted and as a `POST` request to the specified API endpoint in the `main.py` file.  If an image was processed and a DateTime was found, the call would return ```{'date' : '07-05-2005'}```. If there was no `DateTime` tag, `{'date' : 'null'}` is returned.

![sequence_diagram.png](https://github.com/mitch1625/microserviceA/blob/main/sequence_diagram.png)

## Run Locally

Clone the project

```bash
  git clone https://github.com/mitch1625/microserviceA.git
```
Create a virtual environment and install dependencies

```bash
  pip install requirements.txt
```