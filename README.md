# Advanced Hand Gesture Drawing

A sophisticated Python application that allows you to draw on your screen using natural hand gestures captured through your webcam. This project combines computer vision with an intuitive drawing interface for a hands-free creative experience.

![Advanced Hand Gesture Drawing Demo](demo.gif)

## Features

### Core Functionality

- **Thumb-Activated Drawing**: Draw with your index finger **only when your thumb is up**
- **Guidance Mode**: When thumb is down, a guidance point shows where your finger is without drawing
- **Color Selection**: Select different colors by placing your pinky finger on the color palette
- **Multiple Drawing Tools**: Choose between freehand drawing, lines, rectangles, and circles
- **Adjustable Brush Size**: Change the thickness of your drawing strokes
- **Statistics Tracking**: Monitor usage statistics including session time, view count, and more

### Usage Statistics

- **Session Time**: Tracks how long the current drawing session has been active
- **Start Count**: Counts how many times the application has been launched
- **View Count**: Tracks total number of application views
- **Lines Drawn**: Counts the number of drawing strokes created
- **Color Changes**: Tracks how often you change drawing colors

### File Management

- **Save Drawings**: Save your creations as PNG images with timestamps
- **Statistics Persistence**: Your usage statistics are saved between sessions

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
# Create a project directory
mkdir advanced_hand_drawing
cd advanced_hand_drawing

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

### Step 4: Download the Application Code

1. Save the application code as `advanced_hand_drawing.py` in your project directory
2. Ensure you have proper permissions for webcam access

## How to Use

### Starting the Application

```bash
python advanced_hand_drawing.py
```

### Hand Gestures

The application interprets specific hand gestures to control drawing:

1. **Thumb Up + Index Finger**: Activates drawing mode
   - Move your index finger with thumb up to draw on the canvas
2. **Thumb Down + Index Finger**: Guidance mode
   - A gray dot shows where you would draw without actually drawing
   - Use this to position your cursor before drawing
3. **Pinky Finger on Color Palette**: Select a drawing color
   - Place your pinky on the color palette in the top-left corner of the video feed
   - Colors are arranged in a 3×3 grid: red, green, blue, yellow, black, purple, orange, brown, cyan

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

### Statistics Display

The bottom panel shows your usage statistics:

- Current session time
- Application launch count
- Total view count
- Currently selected color
- Number of lines drawn in the current session

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

- **Thumb tip** (landmark #4): Controls drawing mode activation
- **Index finger tip** (landmark #8): Main drawing pointer
- **Pinky finger tip** (landmark #20): Used for color selection

### Performance Considerations

- The application performs best with good lighting conditions
- A minimum of 720p webcam resolution is recommended
- For optimal performance, close other resource-intensive applications
- CPU usage may be high due to real-time video processing

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
   - Check that the color palette is visible in the video feed

## Future Enhancements

### Planned Features

1. **Multi-hand Support**: Draw with both hands simultaneously
2. **Gesture Shortcuts**: Additional gestures for undo/redo operations
3. **Layer Support**: Create and manipulate drawing layers
4. **Image Import**: Draw on top of existing images
5. **Cloud Storage**: Save drawings to cloud services
6. **Voice Commands**: Control the application with voice in addition to gestures
7. **Collaborative Mode**: Draw together with others over a network
8. **3D Drawing**: Extend drawing capabilities to three dimensions
9. **AI-assisted Drawing**: Smart drawing features using machine learning
10. **Export to SVG**: Save drawings in vector format

### Research Directions

- Improved hand tracking in challenging lighting conditions
- More advanced gesture recognition for complex controls
- Reducing system resource requirements for better performance
- Integration with VR/AR environments

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
- [OpenCV](https://opencv.org/) for computer vision capabilities
- [Tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI framework

---

_Note: Replace the demo.gif and hand_landmarks.png placeholder references with actual images once you have created them._
