# Anonymization API with YuNet

## Overview

The Anonymization API utilizes the [OpenCV](https://opencv.org) to detect faces in images and anonymize them by applying a blur.

![preview](/media/screenshot.png "Detection example")

## Installation

To install dependencies, run:

```bash
pip install -r requirements.txt
```

## Usage

To initialize and run the server:

```bash
./core/manage.py migrate && ./core/manage.py runserver
```

## Demo

You can access the API demo here: [https://anon-api.jimmyflatting.com](https://anon-api.jimmyflatting.com)

Note: All uploaded images are stored in a PostgreSQL database.

## Roadmap

Future plans include expanding functionality to support real-time face blurring for live-streamed video via OpenCV.