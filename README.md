# Hand Gesture Drawing App

A Python application that lets you draw on your screen using hand gestures captured through your webcam. This project combines computer vision with drawing functionality to create an interactive and intuitive drawing experience.

![Hand Gesture Drawing Demo](https://github.com/yourusername/hand-gesture-drawing/raw/main/demo.gif)

## Installation

### Prerequisites

- Python 3.7+ installed on your system
- Python 3.10 for best compatibility
- Webcam

### Step 1: Clone the repository

```bash
git clone https://github.com/yourusername/hand-gesture-drawing.git
cd hand-gesture-drawing
```

### Step 2: Create a virtual environment (optional but recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install the required libraries

```bash
pip install opencv-python mediapipe numpy pillow
```

## How to Use

1. Run the application:

```bash
python hand_gesture_drawing.py
```

2. The application will open with two windows:

   - **Left**: Camera feed with hand tracking visualization
   - **Right**: Drawing canvas

3. Basic gestures:
   - **Draw**: Extend both index and middle fingers
   - **Move without drawing**: Extend only the index finger (keep middle finger folded)
   - **Change color**: Use the color dropdown menu
   - **Clear canvas**: Click the "Clear Canvas" button

## How It Works

### Technical Overview

1. **Video Capture**:

   - OpenCV captures video from your webcam

2. **Hand Tracking**:

   - MediaPipe's hand tracking system detects and tracks hand landmarks
   - 21 landmarks are identified on each hand

3. **Gesture Recognition**:

   - Index finger position (landmark #8) determines the drawing position
   - Middle finger extension (landmarks #9 & #12) toggles drawing mode on/off

4. **Drawing Mechanism**:
   - Tkinter canvas maps finger movements to drawing strokes
   - Continuous lines are created by connecting sequential positions

### Code Structure

- `HandGestureDrawingApp` class: Main application class
- `update_frame()`: Processes video frames and detects hand gestures
- `clear_canvas()`: Clears the drawing canvas
- `on_closing()`: Handles cleanup when the application is closed

## Advanced Features (Future Enhancements)

### Already Implemented

- Real-time hand tracking and visualization
- Color selection via dropdown
- Clear canvas functionality

### Planned Features

#### Gesture Controls

- **Pinch gesture (thumb + index)**: Change brush size
- **Fist gesture**: Eraser mode
- **Five fingers extended**: Take screenshot
- **Thumb up**: Undo last stroke
- **Thumb down**: Redo last stroke
- **"OK" sign**: Select color from color wheel

#### Drawing Tools

- **Multiple brush types**: Pencil, marker, calligraphy, etc.
- **Shape tools**: Gesture to switch to rectangle/circle/line drawing mode
- **Text insertion**: Gesture to add text at cursor position
- **Layer support**: Different gestures for layer selection

#### File Operations

- **Save/load functionality**: Gesture to save current drawing
- **Export as different formats**: JPG, PNG, SVG
- **Cloud integration**: Save directly to cloud services

#### User Experience

- **Customizable gestures**: User-defined gesture mappings
- **Adjustable sensitivity**: Settings for different lighting conditions
- **Tutorial mode**: Interactive guidance for new users
- **Voice commands**: Combined voice and gesture control

#### AI Enhancements

- **Gesture prediction**: ML model to improve gesture recognition accuracy
- **Stroke smoothing**: AI-enhanced drawing smoothing
- **Style transfer**: Apply artistic styles to drawings
- **Object recognition**: Auto-enhancement of drawn objects

## Troubleshooting

### Common Issues

1. **Hand detection not working properly**:

   - Ensure you have adequate lighting
   - Keep your hand within the camera frame
   - Move your hand slower for better tracking

2. **Application runs slowly**:

   - Close other resource-intensive applications
   - Reduce the resolution in the code settings
   - Ensure your computer meets the minimum specifications

3. **Installation problems**:
   - Make sure you're using a compatible Python version (3.7+)
   - Update pip: `pip install --upgrade pip`
   - Install dependencies individually if batch install fails

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [MediaPipe](https://google.github.io/mediapipe/) for the hand tracking solution
- [OpenCV](https://opencv.org/) for the computer vision capabilities
- [Tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI framework

---

_Note: The demo GIF placeholder in this README should be replaced with an actual demonstration of your application once implemented._
