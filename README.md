# Hand Gesture Recognition with Computer Vision

A real-time hand gesture recognition system built with Python, OpenCV, and MediaPipe. This project detects and tracks hand movements from webcam input and performs various gesture-based operations.

## Overview

This project demonstrates practical applications of computer vision for hand gesture recognition. It uses MediaPipe's hand tracking solution to identify hand landmarks and interpret gestures in real-time, enabling gesture-based control systems and interactive applications.

## Features

The project includes four distinct applications:

### 1. WhichHand.py
Identifies which hand (left or right) is visible in the camera frame. Detects when both hands are present and displays the appropriate label on screen.

### 2. HighestFinger.py
Tracks all five fingers and identifies which finger is positioned highest in the frame. Displays labeled circles at each fingertip and highlights the highest finger.

### 3. HowManyFingers.py
Counts the number of extended fingers on a detected hand. This implementation includes serial communication support to send finger count data to Arduino devices for hardware integration projects.

### 4. FindPorts.py
Utility script that lists all available serial (COM) ports on your computer. Use this before running HowManyFingers.py to identify the correct port for Arduino communication.

## Requirements

- Python 3.x
- OpenCV (cv2)
- MediaPipe
- pyserial (for Arduino communication)

## Installation

Install the required dependencies:

```bash
pip install opencv-python mediapipe pyserial
```

## Usage

Run any of the scripts from the Main directory:

```bash
python Main/WhichHand.py
python Main/HighestFinger.py
python Main/HowManyFingers.py
```

For Arduino integration:
1. First run `python Main/FindPorts.py` to identify available COM ports
2. Update the port number in HowManyFingers.py (line 7) to match your Arduino's port
3. Run `python Main/HowManyFingers.py`

Press 'q' to quit any running application.

## Technical Details

All scripts use MediaPipe Hands for hand landmark detection with the following configuration:
- Model complexity: 1
- Minimum detection confidence: 0.75
- Minimum tracking confidence: 0.75
- Maximum hands tracked: 2

The system identifies 21 hand landmarks per hand, covering all finger joints and the palm base, enabling precise gesture recognition.

## Future Development

- Enhanced edge case handling for unusual hand positions and angles
- Recognition of more complex hand gestures and sign language
- Multi-gesture command sequences
- Improved lighting tolerance and background handling
