# Advanced Hand Gesture Drawing

![GitHub stars](https://img.shields.io/github/stars/yourusername/hand-gesture-drawing?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/hand-gesture-drawing?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/yourusername/hand-gesture-drawing?style=social)
![GitHub repo size](https://img.shields.io/github/repo-size/yourusername/hand-gesture-drawing)
![GitHub last commit](https://img.shields.io/github/last-commit/yourusername/hand-gesture-drawing)

A sophisticated Python application that allows you to draw on your screen using natural hand gestures captured through your webcam. This project combines computer vision with an intuitive drawing interface for a hands-free creative experience.

![Advanced Hand Gesture Drawing Demo](demo.gif)

## Features

### Core Functionality

- **Thumb-Extension Drawing**: Draw with your index finger when your thumb is extended
- **Guidance Mode**: When thumb is not extended, a guidance point shows where your finger is without drawing
- **Easy Color Selection**: Choose colors from buttons on the right panel or by using your pinky finger on the on-screen color palette
- **Multiple Drawing Tools**: Choose between freehand drawing, lines, rectangles, and circles
- **Adjustable Brush Size**: Change the thickness of your drawing strokes

### Drawing Tools

- **Freehand Drawing**: Draw naturally as if using a pen
- **Line Tool**: Create perfectly straight lines
- **Rectangle Tool**: Draw rectangles with precise corners
- **Circle Tool**: Create perfect circles with customizable size

## Installation

### Prerequisites

- Python 3.10 (recommended) or Python 3.9
- Webcam
- Windows, macOS, or Linux operating system

### Step 1: Set up Python 3.10

#### On Windows:

1. Download Python 3.10 from [python.org](https://www.python.org/downloads/release/python-3109/)
2. Run the installer, checking "Add Python 3.10 to PATH"
3. Verify installation by running `py -3.10 --version` in Command Prompt

#### On macOS:

```bash
brew install python@3.10
```

#### On Linux:

```bash
sudo apt install python3.10 python3.10-venv
```

### Step 2: Create a Project Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/hand-gesture-drawing.git
cd hand-gesture-drawing

# Create a virtual environment
python3.10 -m venv venv

# Activate the environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Required Libraries

```bash
pip install opencv-python mediapipe numpy pillow
```

### Step 4: Run the Application

```bash
python advanced_hand_drawing.py
```

## How to Use

### Hand Gestures

The application interprets specific hand gestures to control drawing:

1. **Extended Thumb + Index Finger**: Activates drawing mode
   - Move your index finger with thumb extended to draw on the canvas
2. **Thumb In Fist + Index Finger**: Guidance mode
   - A gray dot shows where you would draw without actually drawing
   - Use this to position your cursor before drawing
3. **Pinky Finger on Color Palette**: Select a drawing color
   - Place your pinky on the color palette in the right side of the video feed
   - Alternatively, use the color buttons on the right panel of the application

### Drawing Tools

Select different drawing tools from the dropdown menu:

- **Draw**: Freehand drawing (default)
- **Line**: Draw straight lines (first point sets anchor, second point completes line)
- **Rectangle**: Draw rectangles (corners determined by start and end points)
- **Circle**: Draw circles (center at start point, radius determined by end point)

### Interface Controls

- **Clear Canvas**: Erases all drawing from the canvas
- **Save Drawing**: Saves your current drawing as a PNG file
- **Brush Size**: Adjusts the thickness of drawing strokes
- **Mode Selection**: Choose between different drawing tools

## Technical Details

### System Architecture

The application combines several key technologies:

1. **MediaPipe Hands**: Provides accurate hand and finger tracking
2. **OpenCV**: Processes video feed and applies computer vision algorithms
3. **Tkinter**: Provides the graphical user interface and drawing canvas
4. **PIL (Pillow)**: Handles image processing and saving drawings

### Hand Landmark Detection

The application uses MediaPipe's hand landmark detection to track 21 points on your hand:

![Hand Landmarks](hand_landmarks.png)

Key landmarks used:

- **Thumb** (landmarks #1-4): Controls drawing mode activation
- **Index finger tip** (landmark #8): Main drawing pointer
- **Pinky finger tip** (landmark #20): Used for color selection

## Troubleshooting

### Common Issues

1. **Poor hand detection**:

   - Ensure adequate, even lighting on your hand
   - Keep your hand within the camera frame
   - Move your hand slower for better tracking
   - Try adjusting your distance from the camera

2. **Application running slowly**:

   - Close other resource-intensive applications
   - Ensure your computer meets the minimum requirements
   - Try reducing the camera resolution in the code

3. **Colors not selecting properly**:
   - Make sure your pinky finger is clearly visible
   - Hold your pinky still for a moment over the color cell
   - Try using the UI color buttons instead

## Future Enhancements

### Planned Features

1. **Multi-hand Support**: Draw with both hands simultaneously
2. **Gesture Shortcuts**: Additional gestures for undo/redo operations
3. **Layer Support**: Create and manipulate drawing layers
4. **Voice Commands**: Control the application with voice in addition to gestures

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/hand-gesture-drawing&type=Date)](https://star-history.com/#yourusername/hand-gesture-drawing&Date)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [MediaPipe](https://google.github.io/mediapipe/) for the hand tracking solution
- [OpenCV](https://opencv.org/) for computer vision capabilities
- [Tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI framework

---

_Note: Replace "yourusername" in the URLs and badge links with your actual GitHub username when you create the repository. Also, replace the demo.gif and hand_landmarks.png placeholder references with actual images once you have created them._
