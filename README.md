
# Image DateTime Extractor

This microservice receives an image in `.jpg`, `.jpeg`, or `.png` format and extracts the “Exif.Image.DateTime” from the exif metadata of the image. The information is returned as JSON.
If DateTime is present, `{'date' : 'MM-DD-YYYY}` is returned, where `MM-DD-YYYY` is the DateTime information extracted. If DateTime is not present or the file is a specified file extension, ```{'date' : 'null'}``` is returned.

1. This microservice continuously monitors a specified directory. Once a file is placed into that directory, that file is processed for Image.DateTime data.

2. The extracted data is automatically returned as a `POST` request to the specified API endpoint in the `main.py` file.  If an image was processed and a DateTime was found, the call would return ```{'date' : '07-05-2005'}```.


![sequence_diagram.png](sequence_diagram.png)
## Run Locally

Clone the project

```bash
  git clone https://github.com/mitch1625/microserviceA.git
```
Create a virtual environment and install dependencies

```bash
  pip install requirements.txt
```

In `main.py` change:
- `PATH` - the directory name to look for files 
- `API_ENDPOINT` - point the endpoint in your API
