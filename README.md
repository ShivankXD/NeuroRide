# NeuroRide : Ensuring Road Safety with Deep Learning

###

<img src="https://github.com/ShivankXD/ShivankXD/blob/main/NeuroRidedet.png" style="max-width: 100%; height: auto;">

###

## Overview
NeuroRide is an AI-powered computer vision project designed to detect helmets and number plates in real-time video streams. It identifies motorcyclists without helmets and marks their number plates for further processing.

## Features
- Helmet Detection: Detects whether a rider is wearing a helmet.
- Number Plate Recognition: Uses OCR to extract number plate details.
- Automated Processing: Marks number plates of violators and tracks them.
- User Interface: Clicking a button moves detected number plates to a list with a path-tracing effect, while the video continues playing in a mini-player.

## Tech Stack
- Programming Language: Python
- Libraries & Frameworks: OpenCV, TensorFlow/PyTorch, Ultralytics YOLO, EasyOCR
- UI Framework: Streamlit/Flask

## Installation
1. Clone the Repository :
 ``` shell []
git clone https://github.com/yourusername/NeuroRide.git
cd NeuroRide

```

2. Install Dependencies:
``` shell
pip install -r requirements.txt

```

3. Download & Set Up Weights:
- Place YOLO model weights in the models/ folder.

4. Run the Application:
``` shell
 python app.py

```


## Usage
1. Upload or stream a video feed.
2. The model detects helmets and number plates.
3. Violators' number plates are moved to a list with path tracing.
4. Export the list of violators for further action.

## Future Enhancements
- Integration with government databases for automated fine generation.
- Real-time tracking through CCTV networks.
- Web-based dashboard for monitoring violations.


