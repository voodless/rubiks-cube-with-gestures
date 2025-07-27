# Gesture-Controlled Rubik's Cube 

A Python-based 2x2 Rubik's Cube simulator with both keyboard and gesture-based controls using computer vision and machine learning. Control the cube with hand gestures captured through your webcam.

## Built For

This project was created for the boot.dev hackathon, showcasing the integration of computer vision, machine learning, and interactive gaming..


## Features

- **Dual Input Modes**: Choose between keyboard (WASD) or gesture controls
- **Real-time Gesture Recognition**: Uses MediaPipe for accurate hand gesture detection
- **Visual Cube Representation**: Full-color terminal display with both net and 3D views
- **Smart Camera Detection**: Automatically finds and configures your camera
- **Cross-platform Support**: Works on macOS, Windows, and Linux
- **Undo Functionality**: Built-in move history and undo system

## Demo

The cube responds to these gestures:
- **Thumbs Up** → Rotate top face clockwise (W)
- **Thumbs Down** → Rotate bottom face clockwise (S) 
- **Closed Fist** → Rotate left face clockwise (A)
- **Open Palm** → Rotate right face clockwise (D)
- **Victory Sign** → Exit application

## Requirements

```
opencv-python
mediapipe
tensorflow
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/voodless/rubiks-cube-with-gestures.git
cd rubiks-cube-with-gestures
```

2. Install dependencies:
```bash
pip install opencv-python mediapipe tensorflow
```

3. Download the MediaPipe gesture recognition model:
   - The model file `gesture_recognizer.task` should be placed in `src/assets/`
   - Update the `gesture_path` variable in the main script to match your file location

## Usage

Run the main application:
```bash
python main.py
```

### Input Modes

**1. WASD Mode (Keyboard)**
- W: Rotate top face clockwise
- A: Rotate left face clockwise  
- S: Rotate bottom face clockwise
- D: Rotate right face clockwise
- 'fail': Undo all moves and exit
- 'exit': Exit application
- 'm': Return to mode selection

**2. Gesture Mode (Camera)**
- Perform hand gestures in front of your camera
- The system will detect and translate gestures to cube moves
- Press 'q' in the camera window or type 'exit' to return to mode selection

### Game Commands
- **Solve Detection**: Automatically detects when the cube is solved
- **Scrambling**: Cube starts with a 15-move pseudo-random scramble
- **Move History**: All moves are tracked and can be undone

## Project Structure

```
rubiks-cube-with-gestures/
├── main.py              # Main application entry point
├── cube_logic.py        # 2x2 Rubik's cube logic and state management
├── cube_renderer.py     # Colorized ASCII visualization of the cube
├── gesture_detector.py  # MediaPipe gesture recognition system
└── src/assets/
    └── gesture_recognizer.task  # MediaPipe model file
```

## Technical Details

### Cube Logic
- Implements a complete 2x2 Rubik's Cube with proper face rotations and corner orientations
- Full color mapping system: White (U), Yellow (D), Red (F), Orange (B), Green (L), Blue (R)
- Dual visualization modes: cube net layout and 3D perspective view
- Tracks move history for undo functionality
- Includes solve state detection and pseudo-random scrambling

### Camera Handling
- Uses MediaPipe's pre-trained gesture recognition model
- Processes camera input in real-time at 30 FPS
- Confidence threshold of 0.3 for gesture detection
- Hand landmark visualization for debugging

### Visual Display
- **Cube Net View**: Traditional unfolded cube layout showing all 6 faces
- **3D Perspective View**: Isometric representation showing 3 visible faces
- **Full Color Support**: Each face displays in its actual cube colors using terminal escape codes
- **Corner-based Rendering**: Accurate representation of corner piece positions and orientations
- Automatically detects available cameras across different indices
- Prioritizes AVFoundation backend on macOS for better compatibility
- Configurable resolution (640x480) and frame rate (30 FPS)

## Troubleshooting

**Camera Issues:**
- Ensure your camera is not being used by another application
- Try running with different camera indices if detection fails
- On macOS, grant camera permissions to your terminal/IDE

**Gesture Recognition:**
- Ensure good lighting for optimal hand detection
- Keep your hand clearly visible in the camera frame
- Gestures need to be held briefly for recognition

**Dependencies:**
- If TensorFlow warnings appear, they're suppressed but the app will still work
- Ensure all required packages are installed with compatible versions
