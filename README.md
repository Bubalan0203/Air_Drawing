# Air Drawing Application - Project Documentation

## Overview
The **Air Drawing Application** allows users to draw virtually in the air using hand gestures captured through a webcam. The system uses computer vision and machine learning to recognize hand gestures and convert them into drawing commands.

## Technologies Used
- **Python 3**: The main programming language used for scripting the entire application.
- **OpenCV**: A powerful computer vision library used to capture video feed, detect hand movements, and draw on frames.
- **MediaPipe**: A framework developed by Google for building perception pipelines. Used here for hand landmark detection to accurately track finger movements.
- **NumPy**: A library for numerical operations, used to manage arrays and coordinate calculations efficiently.
- **PyAudio**: Required for capturing microphone input in real-time.
- **SpeechRecognition**: A library to recognize voice commands by converting speech into text.
- **Virtual Environment (venv)**: Ensures isolated Python environment for dependencies to avoid version conflicts.

## Folder Structure
```
code/
├── air_drawing.py          # Main controller file
├── hand_tracking.py        # Hand tracking logic using MediaPipe
├── gesture_recognition.py  # Gesture recognition logic
├── drawing_utils.py        # Drawing utilities
├── ui_elements.py          # UI buttons and interface elements
```

## File Descriptions
### `air_drawing.py`
- Main entry point of the application
- Captures webcam feed using OpenCV
- Uses `HandTracking` class to detect hand landmarks
- Passes landmarks to `GestureRecognition` to identify gestures
- Based on recognized gestures, calls `DrawingUtils` to draw
- Displays UI from `UIElements`
- Captures voice input using `SpeechRecognition` and `PyAudio`

### `hand_tracking.py`
- Initializes MediaPipe hand model
- Processes video frames to detect hand and return finger positions
- Sends coordinates to the gesture recognizer

### `gesture_recognition.py`
- Identifies gesture patterns like:
  - Index finger up → draw mode
  - All fingers down → stop drawing
  - Open palm → clear screen
- Provides current gesture state to the main file

### `drawing_utils.py`
- Handles drawing actions such as:
  - Drawing lines between finger points
  - Changing brush color/size
  - Erasing canvas
- Maintains draw history for undo/clear operations

### `ui_elements.py`
- Defines on-screen buttons (color pickers, size changers)
- Handles logic when a finger clicks on any UI element
![Flow](https://github.com/user-attachments/assets/8f6a1a31-2176-450d-8230-cce3bb84d615)

## How the App Works (Flowchart Summary)
1. **Video Frame Capture** → `OpenCV` continuously captures webcam frames
2. **Hand Detection** → `MediaPipe` detects hand and provides landmarks
3. **Gesture Recognition** → `gesture_recognition.py` identifies gestures
4. **Voice Command Recognition** → `SpeechRecognition` interprets audio input
5. **Command Execution** → Based on voice/gesture, `drawing_utils.py` is triggered
6. **Drawing on Canvas** → Updated frame is drawn and shown on screen
7. **User Interaction with UI** → `ui_elements.py` reacts to finger tap-like gestures

## How to Set Up and Run
### Step 1: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### Step 2: Install Required Libraries
```bash
pip install opencv-python mediapipe numpy pyaudio SpeechRecognition
```

### Step 3: Run the App
```bash
python air_drawing.py
```

## Usage Guide
- Raise index finger to begin drawing
- Close all fingers to stop
- Show open palm to clear screen
- Move hand to buttons to change brush or color
- Use microphone and say commands like:
  - "clear canvas"
  - "change color to blue"
  - "increase brush size"

## Features
- Draw without touching the screen
- Change color and brush dynamically
- Clear screen with gesture or voice
- Real-time video with minimal delay
- Interactive virtual UI for controls

## Learning Outcomes
- Learn to work with **OpenCV** for video streaming and drawing
- Use **MediaPipe** for real-time hand tracking
- Build gesture recognition logic
- Integrate **voice recognition** using PyAudio & SpeechRecognition
- Develop an intuitive UI using hand gestures
- Structure a Python project with modular architecture

## Conclusion
This Air Drawing project is a creative way to explore the possibilities of computer vision and voice control. It integrates multiple cutting-edge libraries and teaches how to combine them into a seamless, interactive Python application. Whether for education, entertainment, or prototyping gesture interfaces, this project serves as a solid foundation.

> By learning and running this project, users gain valuable experience in real-time image processing, gesture-based UI, and speech interaction systems — skills widely applicable in modern AI and user experience design.

