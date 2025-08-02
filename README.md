
# Image DateTime Extractor

This microservice receives an image in `.jpg`, `.jpeg`, or `.png` format and extracts the “Exif.Image.DateTime” from the exif metadata of the image. It returns this data as a single line JSON-formatted response with the date in MM-DD-YYYY format.



## Run Locally

Clone the project

```bash
  git clone https://github.com/mitch1625/microserviceA.git
```

Go to the project directory

```bash
  cd teammateMicroservice
```

Create a virtual environment and install dependencies

```bash
  pip install requirements.txt
```

In `main.py` change:
- `PATH` - the directory name to look for files 
- `API_ENDPOINT` - point the endpoint in your API
