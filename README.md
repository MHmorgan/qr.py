# qr.py

Generate QR codes with python.

Created by vibe coding 🏖️

## Usage

```
usage: qr.py [-h] [-s {square,rounded,dots,gapped,vertical,horizontal}]
             [-f FILL_COLOR] [-b BACK_COLOR] [--version]
             url file_output

Generate a QR code from a URL and save it to a file.

positional arguments:
  url                   The URL or text to encode in the QR code
  file_output           Output file path (format detected from extension)

options:
  -h, --help            show this help message and exit
  -s, --style {square,rounded,dots,gapped,vertical,horizontal}
                        Style of QR code modules (default: square)
  -f, --fill-color FILL_COLOR
                        Color of QR code modules (default: black). Supports
                        hex (#RRGGBB), named colors, or RGB (255,0,0)
  -b, --back-color BACK_COLOR
                        Background color (default: white). Supports hex
                        (#RRGGBB), named colors, or RGB (255,0,0)
  --version             show program's version number and exit

Supported formats: PNG, JPEG, BMP, GIF, TIFF, WEBP, ICO
Colors: hex (#RRGGBB), named (red, blue), or RGB (255,0,0)
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

