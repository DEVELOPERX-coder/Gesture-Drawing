import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import time
import json
import os
from datetime import datetime

class AdvancedHandGestureDrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Hand Gesture Drawing")
        
        # Simplified app initialization
        self.session_start = datetime.now()
        self.lines_drawn = 0
        
        # Set up frames
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill="both", expand=True)
        
        self.video_frame = tk.Frame(self.main_frame)
        self.video_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Color palette frame on the right side
        self.color_frame = tk.Frame(self.main_frame)
        self.color_frame.pack(side=tk.RIGHT, fill="y", padx=10, pady=10)
        
        self.canvas_frame = tk.Frame(self.main_frame)
        self.canvas_frame.pack(side=tk.RIGHT, fill="both", expand=True, padx=10, pady=10)
        
        # Video display
        self.video_label = tk.Label(self.video_frame, text="Initializing camera...")
        self.video_label.pack()
        
        # Canvas for drawing
        self.canvas = tk.Canvas(self.canvas_frame, bg="white", width=640, height=480)
        self.canvas.pack(fill="both", expand=True)
        
        # Status bar
        self.status_bar = tk.Label(self.canvas_frame, text="Ready. Thumb up to draw with index finger.", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill="x")
        
        # Control panel
        self.controls = tk.Frame(root)
        self.controls.pack(side=tk.BOTTOM, fill="x", pady=5)
        
        # Clear canvas button
        self.clear_button = ttk.Button(self.controls, text="Clear Canvas", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT, padx=10)
        
        # Save drawing button
        self.save_button = ttk.Button(self.controls, text="Save Drawing", command=self.save_drawing)
        self.save_button.pack(side=tk.LEFT, padx=10)
        
        # Mode selection
        self.mode_var = tk.StringVar(value="draw")
        ttk.Label(self.controls, text="Mode:").pack(side=tk.LEFT, padx=(20, 5))
        self.mode_menu = ttk.Combobox(self.controls, textvariable=self.mode_var, 
                                     values=["draw", "line", "rectangle", "circle"], 
                                     state="readonly", width=10)
        self.mode_menu.pack(side=tk.LEFT, padx=5)
        
        # Brush size
        ttk.Label(self.controls, text="Brush Size:").pack(side=tk.LEFT, padx=(20, 5))
        self.brush_size_var = tk.IntVar(value=3)
        self.brush_size_slider = ttk.Scale(self.controls, from_=1, to=20, 
                                         variable=self.brush_size_var, orient=tk.HORIZONTAL, 
                                         length=100)
        self.brush_size_slider.pack(side=tk.LEFT, padx=5)
        
        # Simple status display
        self.status_var = tk.StringVar(value="Current Color: black")
        self.status_label = ttk.Label(self.controls, textvariable=self.status_var)
        self.status_label.pack(side=tk.RIGHT, padx=10)
        
        # Drawing state variables
        self.drawing = False
        self.prev_x, self.prev_y = None, None
        self.start_point = None  # For shapes like rectangles, circles
        self.current_color = "black"
        
        # Available colors for selection with pinky finger
        self.colors = {
            "bottom_left": "red",
            "bottom_center": "green",
            "bottom_right": "blue",
            "mid_left": "yellow",
            "mid_center": "black",
            "mid_right": "purple",
            "top_left": "orange",
            "top_center": "brown",
            "top_right": "cyan"
        }
        
        # MediaPipe hands setup
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Virtual color palette
        self.color_palette = self.create_color_palette()
        
        # Start video capture
        self.cap = cv2.VideoCapture(0)
        self.update_frame()
        
        # Start session timer
        self.update_session_timer()
    
    def create_color_palette(self):
        """Create UI color buttons in the side panel"""
        colors = [
            ("red", "#FF0000"),
            ("green", "#00FF00"),
            ("blue", "#0000FF"),
            ("yellow", "#FFFF00"),
            ("black", "#000000"),
            ("purple", "#800080"),
            ("orange", "#FFA500"),
            ("brown", "#A52A2A"),
            ("cyan", "#00FFFF")
        ]
        
        # Create color buttons
        self.color_buttons = []
        for name, hex_color in colors:
            btn = tk.Button(self.color_frame, 
                           background=hex_color, 
                           width=3, height=1,
                           command=lambda c=name: self.set_color(c))
            btn.pack(pady=5, padx=10, fill="x")
            self.color_buttons.append((name, btn))
            
            # Add tooltip-like label
            lbl = tk.Label(self.color_frame, text=name)
            lbl.pack(pady=0, padx=10)
        
        # Also create a virtual color palette for the video feed
        palette = np.ones((480, 50, 3), dtype=np.uint8) * 255
        
        # Vertical strips of colors
        cell_h = 480 // len(colors)
        for i, (name, hex_color) in enumerate(colors):
            # Convert hex to BGR (OpenCV uses BGR)
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            
            y1, y2 = i * cell_h, (i + 1) * cell_h
            palette[y1:y2, :] = (b, g, r)  # BGR format for OpenCV
        
        return palette
        
    def set_color(self, color_name):
        """Set the current drawing color when a color button is clicked"""
        self.current_color = color_name
        self.status_var.set(f"Current Color: {color_name}")
        self.status_bar.config(text=f"Color selected: {color_name}")
    
    # Remove the statistics-related methods that are no longer needed
    
    def clear_canvas(self):
        """Clear the canvas"""
        self.canvas.delete("all")
        self.status_bar.config(text="Canvas cleared. Thumb up to draw with index finger.")
    
    def save_drawing(self):
        """Save the current drawing to a file"""
        # Get canvas dimensions
        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        
        # Create filename with timestamp
        filename = f"drawing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        try:
            # Take screenshot of canvas area
            ImageTk.PhotoImage(self.canvas).save(filename)
            self.status_bar.config(text=f"Drawing saved as {filename}")
        except:
            # Alternative method using PIL
            try:
                import pyscreenshot as ImageGrab
                ImageGrab.grab(bbox=(x, y, x1, y1)).save(filename)
                self.status_bar.config(text=f"Drawing saved as {filename}")
            except:
                self.status_bar.config(text="Error saving drawing. Screenshot functionality may not be available.")
    
    def update_frame(self):
        """Update video frame and process hand tracking"""
        ret, frame = self.cap.read()
        if ret:
            # Flip the frame horizontally for a more intuitive mirror view
            frame = cv2.flip(frame, 1)
            
            # Overlay the color palette on the right side of the frame
            h, w, _ = self.color_palette.shape
            right_edge = frame.shape[1] - w - 10
            roi = frame[10:10+h, right_edge:right_edge+w]
            
            # Only try to blend if ROI is valid
            if roi.shape[0] > 0 and roi.shape[1] > 0:
                # Create a mask from the palette for proper overlay
                palette_gray = cv2.cvtColor(self.color_palette, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(palette_gray, 1, 255, cv2.THRESH_BINARY)
                mask_inv = cv2.bitwise_not(mask)
                
                # Now blend the palette with the original frame
                try:
                    frame_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
                    palette_fg = cv2.bitwise_and(self.color_palette, self.color_palette, mask=mask)
                    frame[10:10+h, right_edge:right_edge+w] = cv2.add(frame_bg, palette_fg)
                except:
                    # If there's a shape mismatch or other error, just overlay directly
                    if h <= frame.shape[0] - 10 and w <= frame.shape[1] - right_edge:
                        frame[10:10+h, right_edge:right_edge+w] = self.color_palette
                
            # Add text labels to show what each color is
            cv2.putText(frame, "Colors", (right_edge + 5, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            
            # Convert the BGR image to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_h, frame_w, _ = frame.shape
            
            # Process the frame with MediaPipe
            results = self.hands.process(rgb_frame)
            
            # Draw hand landmarks on the frame
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw hand landmarks
                    self.mp_drawing.draw_landmarks(
                        frame, 
                        hand_landmarks, 
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing_styles.get_default_hand_landmarks_style(),
                        self.mp_drawing_styles.get_default_hand_connections_style()
                    )
                    
                    # Get landmark positions
                    landmarks = {}
                    for i, landmark in enumerate(hand_landmarks.landmark):
                        x_px = min(int(landmark.x * frame_w), frame_w - 1)
                        y_px = min(int(landmark.y * frame_h), frame_h - 1)
                        landmarks[i] = (x_px, y_px)
                    
                    # Get position of important fingers and finger landmarks
                    thumb_tip = landmarks[self.mp_hands.HandLandmark.THUMB_TIP.value]
                    thumb_ip = landmarks[self.mp_hands.HandLandmark.THUMB_IP.value]
                    thumb_mcp = landmarks[self.mp_hands.HandLandmark.THUMB_MCP.value]
                    index_tip = landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP.value]
                    index_dip = landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_DIP.value]
                    pinky_tip = landmarks[self.mp_hands.HandLandmark.PINKY_TIP.value]
                    wrist = landmarks[self.mp_hands.HandLandmark.WRIST.value]
                    
                    # Detect if thumb is extended (distance from thumb tip to wrist is significantly greater than distance from MCP to wrist)
                    thumb_wrist_dist = ((thumb_tip[0] - wrist[0])**2 + (thumb_tip[1] - wrist[1])**2)**0.5
                    thumb_mcp_wrist_dist = ((thumb_mcp[0] - wrist[0])**2 + (thumb_mcp[1] - wrist[1])**2)**0.5
                    
                    # Thumb is considered extended if its tip is significantly further from the wrist than the MCP
                    thumb_is_extended = thumb_wrist_dist > thumb_mcp_wrist_dist * 1.2
                    
                    # Check if pinky is in the color palette area (now on the right side)
                    right_edge = frame.shape[1] - self.color_palette.shape[1] - 10
                    in_palette_area = (right_edge <= pinky_tip[0] <= right_edge + self.color_palette.shape[1] and 
                                       10 <= pinky_tip[1] <= 10 + self.color_palette.shape[0])
                    
                    # Select color with pinky finger if in palette area
                    if in_palette_area:
                        # The color palette is now vertical, so we only need the y-coordinate
                        rel_y = (pinky_tip[1] - 10) // (self.color_palette.shape[0] // len(self.colors))
                        
                        # Make sure rel_y is in valid range
                        if 0 <= rel_y < len(self.colors):
                            # Get color name from list of colors (keys of self.colors dict, ordered)
                            color_names = list(self.colors.values())
                            new_color = color_names[rel_y]
                            
                            if new_color != self.current_color:
                                self.current_color = new_color
                                self.status_var.set(f"Current Color: {self.current_color}")
                                self.status_bar.config(text=f"Color selected: {self.current_color}")
                    
                    # Draw a circle at the index finger tip
                    cv2.circle(frame, index_tip, 10, (0, 255, 0), -1)
                    
                    # Map the finger coordinates to the canvas
                    canvas_x, canvas_y = index_tip
                    
                    # Drawing mode depends on thumb extension
                    current_mode = self.mode_var.get()
                    
                    if thumb_is_extended:
                        # Draw mode (thumb is extended)
                        cv2.circle(frame, thumb_tip, 10, (0, 0, 255), -1)
                        cv2.putText(frame, "Drawing Mode", (frame_w - 150, 30), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                        
                        if not self.drawing:
                            self.drawing = True
                            self.prev_x, self.prev_y = None, None
                            self.start_point = (canvas_x, canvas_y)
                            self.status_bar.config(text=f"Drawing with {self.current_color}. Mode: {current_mode}")
                        
                        if current_mode == "draw":
                            # Free drawing mode
                            if self.prev_x is not None and self.prev_y is not None:
                                self.canvas.create_line(
                                    self.prev_x, self.prev_y, canvas_x, canvas_y,
                                    width=self.brush_size_var.get(), fill=self.current_color, 
                                    capstyle=tk.ROUND, smooth=True
                                )
                                self.lines_drawn += 1
                        elif current_mode == "line" and self.start_point is not None:
                            # Line drawing mode
                            self.canvas.delete("temp_shape")
                            self.canvas.create_line(
                                self.start_point[0], self.start_point[1], canvas_x, canvas_y,
                                width=self.brush_size_var.get(), fill=self.current_color,
                                tags="temp_shape"
                            )
                        elif current_mode == "rectangle" and self.start_point is not None:
                            # Rectangle drawing mode
                            self.canvas.delete("temp_shape")
                            self.canvas.create_rectangle(
                                self.start_point[0], self.start_point[1], canvas_x, canvas_y,
                                width=self.brush_size_var.get(), outline=self.current_color,
                                tags="temp_shape"
                            )
                        elif current_mode == "circle" and self.start_point is not None:
                            # Circle drawing mode
                            self.canvas.delete("temp_shape")
                            radius = ((canvas_x - self.start_point[0])**2 + 
                                      (canvas_y - self.start_point[1])**2)**0.5
                            self.canvas.create_oval(
                                self.start_point[0] - radius, self.start_point[1] - radius,
                                self.start_point[0] + radius, self.start_point[1] + radius,
                                width=self.brush_size_var.get(), outline=self.current_color,
                                tags="temp_shape"
                            )
                        
                        self.prev_x, self.prev_y = canvas_x, canvas_y
                    else:
                        # Not drawing mode (thumb is down/sideways)
                        if self.drawing:
                            # Finish the shape if we were drawing one
                            if current_mode != "draw" and self.start_point is not None:
                                self.canvas.delete("temp_shape")
                                if current_mode == "line":
                                    self.canvas.create_line(
                                        self.start_point[0], self.start_point[1], self.prev_x, self.prev_y,
                                        width=self.brush_size_var.get(), fill=self.current_color
                                    )
                                elif current_mode == "rectangle":
                                    self.canvas.create_rectangle(
                                        self.start_point[0], self.start_point[1], self.prev_x, self.prev_y,
                                        width=self.brush_size_var.get(), outline=self.current_color
                                    )
                                elif current_mode == "circle":
                                    radius = ((self.prev_x - self.start_point[0])**2 + 
                                             (self.prev_y - self.start_point[1])**2)**0.5
                                    self.canvas.create_oval(
                                        self.start_point[0] - radius, self.start_point[1] - radius,
                                        self.start_point[0] + radius, self.start_point[1] + radius,
                                        width=self.brush_size_var.get(), outline=self.current_color
                                    )
                                self.lines_drawn += 1
                            
                            self.drawing = False
                            self.start_point = None
                            self.status_bar.config(text="Guidance mode. Thumb up to start drawing.")
                        
                        # Draw a guidance point on the canvas
                        self.canvas.delete("guidance_point")
                        self.canvas.create_oval(
                            canvas_x - 5, canvas_y - 5, canvas_x + 5, canvas_y + 5,
                            fill="gray", outline="black", tags="guidance_point"
                        )
                        
                        # Display guidance mode in frame
                        cv2.putText(frame, "Guidance Mode", (frame_w - 150, 30), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (128, 128, 128), 2)
            
            # Convert the frame to a format suitable for tkinter
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        
        # Schedule the next update
        self.root.after(10, self.update_frame)
    
    def on_closing(self):
        """Handle cleanup when the application is closed"""
        self.cap.release()
        self.hands.close()
        self.root.destroy()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedHandGestureDrawingApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()