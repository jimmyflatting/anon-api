# Anonymization API with YuNet

## Overview

The Anonymization API utilizes the YuNet model to detect faces in images and anonymize them by applying a blur. Currently, the model returns x and y coordinates for facial landmarks, which may need to be remapped to a -1 to 1 scale for better performance due to image size variations.

![preview](/repo-assets/ana.png "Detection example")

## Installation

To install dependencies, run:

```bash
pip install -r requirements.txt
```

## Usage

To initialize and run the server:

```bash
./anon_api/manage.py migrate && ./anon_api/manage.py runserver
```

## Demo

You can access the API demo here: [anon.foreversegfault.com](https://anon.foreversegfault.com)

Note: All uploaded images are stored in a PostgreSQL database.

## Credits

Model credits: [YuNet](https://github.com/ShiqiYu/libfacedetection)

## Roadmap

Future plans include expanding functionality to support real-time face blurring for live-streamed video via OpenCV.