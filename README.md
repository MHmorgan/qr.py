# qr.py

Generate QR codes with python.

## Usage

```
usage: qr.py [-h] [--version] url file_output

Generate a QR code from a URL and save it to a file.

positional arguments:
  url          The URL or text to encode in the QR code
  file_output  Output file path (format detected from extension)

options:
  -h, --help   show this help message and exit
  --version    show program's version number and exit

Supported formats: PNG, JPEG, BMP, GIF, TIFF, WEBP, ICO
```


### [Poetry](https://python-poetry.org/)

```shell
poetry update
poetry run python qr.py www.example.com qr.png
```

### Plain

```shell
pip install "qrcode[pil]"
./qr.py www.example.com qr.png
```

