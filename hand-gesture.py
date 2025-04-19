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
        
        # Application stats
        self.stats = {
            'session_start': datetime.now(),
            'start_count': 0,
            'view_count': 1,  # Current session counts as 1
            'total_drawing_time': 0,
            'color_changes': 0,
            'lines_drawn': 0
        }
        
        # Load previous stats if available
        self.load_stats()
        
        # Set up frames
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill="both", expand=True)
        
        self.video_frame = tk.Frame(self.main_frame)
        self.video_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.canvas_frame = tk.Frame(self.main_frame)
        self.canvas_frame.pack(side=tk.RIGHT, fill="both", expand=True, padx=10, pady=10)
        
        # Stats display frame
        self.stats_frame = tk.Frame(root)
        self.stats_frame.pack(side=tk.BOTTOM, fill="x")
        
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
        
        # Stats display
        self.stats_display = ttk.LabelFrame(self.stats_frame, text="Session Statistics")
        self.stats_display.pack(fill="x", padx=10, pady=5)
        
        self.stats_text = {
            'session_time': tk.StringVar(value="Session Time: 00:00"),
            'start_count': tk.StringVar(value=f"Start Count: {self.stats['start_count']}"),
            'view_count': tk.StringVar(value=f"View Count: {self.stats['view_count']}"),
            'current_color': tk.StringVar(value="Current Color: black"),
            'lines_drawn': tk.StringVar(value="Lines Drawn: 0")
        }
        
        # Create stats labels
        stats_inner_frame = tk.Frame(self.stats_display)
        stats_inner_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(stats_inner_frame, textvariable=self.stats_text['session_time']).pack(side=tk.LEFT, padx=10)
        ttk.Label(stats_inner_frame, textvariable=self.stats_text['start_count']).pack(side=tk.LEFT, padx=10)
        ttk.Label(stats_inner_frame, textvariable=self.stats_text['view_count']).pack(side=tk.LEFT, padx=10)
        ttk.Label(stats_inner_frame, textvariable=self.stats_text['current_color']).pack(side=tk.LEFT, padx=10)
        ttk.Label(stats_inner_frame, textvariable=self.stats_text['lines_drawn']).pack(side=tk.LEFT, padx=10)
        
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
        """Create a color palette image that will be displayed on screen"""
        palette = np.ones((180, 180, 3), dtype=np.uint8) * 255
        
        # Grid of colors (3x3)
        cell_h, cell_w = 60, 60
        colors = [
            [(255, 165, 0), (165, 42, 42), (0, 255, 255)],  # orange, brown, cyan
            [(255, 255, 0), (0, 0, 0), (128, 0, 128)],      # yellow, black, purple
            [(255, 0, 0), (0, 255, 0), (0, 0, 255)]         # red, green, blue
        ]
        
        for i in range(3):
            for j in range(3):
                y1, y2 = i * cell_h, (i + 1) * cell_h
                x1, x2 = j * cell_w, (j + 1) * cell_w
                palette[y1:y2, x1:x2] = colors[i][j][::-1]  # Reverse BGR for OpenCV
        
        return palette
    
    def load_stats(self):
        """Load previous statistics if available"""
        if os.path.exists("drawing_stats.json"):
            try:
                with open("drawing_stats.json", "r") as f:
                    saved_stats = json.load(f)
                    if 'start_count' in saved_stats:
                        self.stats['start_count'] = saved_stats['start_count'] + 1
                    if 'view_count' in saved_stats:
                        self.stats['view_count'] = saved_stats['view_count'] + 1
                    if 'total_drawing_time' in saved_stats:
                        self.stats['total_drawing_time'] = saved_stats['total_drawing_time']
            except:
                # If error in reading stats, continue with defaults
                pass
    
    def save_stats(self):
        """Save current statistics to file"""
        # Calculate session time
        session_time = (datetime.now() - self.stats['session_start']).total_seconds()
        self.stats['total_drawing_time'] += session_time
        
        try:
            with open("drawing_stats.json", "w") as f:
                json.dump(self.stats, f)
        except:
            # If error in saving stats, just continue
            pass
    
    def update_session_timer(self):
        """Update the session timer display"""
        session_duration = datetime.now() - self.stats['session_start']
        minutes, seconds = divmod(session_duration.seconds, 60)
        self.stats_text['session_time'].set(f"Session Time: {minutes:02d}:{seconds:02d}")
        self.root.after(1000, self.update_session_timer)
    
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
            
            # Overlay the color palette in the top-left corner
            h, w, _ = self.color_palette.shape
            roi = frame[10:10+h, 10:10+w]
            # Create a mask from the palette for proper overlay
            palette_gray = cv2.cvtColor(self.color_palette, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(palette_gray, 1, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)
            
            # Now blend the palette with the original frame
            frame_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
            palette_fg = cv2.bitwise_and(self.color_palette, self.color_palette, mask=mask)
            frame[10:10+h, 10:10+w] = cv2.add(frame_bg, palette_fg)
            
            # Add text labels to show what each color is
            cv2.putText(frame, "Colors:", (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            
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
                    
                    # Get position of important fingers
                    thumb_tip = landmarks[self.mp_hands.HandLandmark.THUMB_TIP.value]
                    thumb_mcp = landmarks[self.mp_hands.HandLandmark.THUMB_MCP.value]
                    index_tip = landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP.value]
                    pinky_tip = landmarks[self.mp_hands.HandLandmark.PINKY_TIP.value]
                    wrist = landmarks[self.mp_hands.HandLandmark.WRIST.value]
                    
                    # Detect if thumb is up (y-coordinate of thumb tip is significantly less than MCP)
                    thumb_is_up = thumb_tip[1] < thumb_mcp[1] - 20
                    
                    # Check if pinky is in the color palette area
                    in_palette_area = (10 <= pinky_tip[0] <= 10 + self.color_palette.shape[1] and 
                                      10 <= pinky_tip[1] <= 10 + self.color_palette.shape[0])
                    
                    # Select color with pinky finger if in palette area
                    if in_palette_area:
                        # Determine which color cell the pinky is in
                        rel_x = (pinky_tip[0] - 10) // 60  # 60 is cell width
                        rel_y = (pinky_tip[1] - 10) // 60  # 60 is cell height
                        
                        if 0 <= rel_x < 3 and 0 <= rel_y < 3:
                            # Map to color names
                            regions = [
                                ["top_left", "top_center", "top_right"],
                                ["mid_left", "mid_center", "mid_right"],
                                ["bottom_left", "bottom_center", "bottom_right"]
                            ]
                            color_region = regions[rel_y][rel_x]
                            new_color = self.colors[color_region]
                            
                            if new_color != self.current_color:
                                self.current_color = new_color
                                self.stats_text['current_color'].set(f"Current Color: {self.current_color}")
                                self.status_bar.config(text=f"Color selected: {self.current_color}")
                                self.stats['color_changes'] += 1
                    
                    # Draw a circle at the index finger tip
                    cv2.circle(frame, index_tip, 10, (0, 255, 0), -1)
                    
                    # Map the finger coordinates to the canvas
                    canvas_x, canvas_y = index_tip
                    
                    # Drawing mode depends on thumb position
                    current_mode = self.mode_var.get()
                    
                    if thumb_is_up:
                        # Draw mode (thumb is up)
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
                                self.stats['lines_drawn'] += 1
                                self.stats_text['lines_drawn'].set(f"Lines Drawn: {self.stats['lines_drawn']}")
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
                                self.stats['lines_drawn'] += 1
                                self.stats_text['lines_drawn'].set(f"Lines Drawn: {self.stats['lines_drawn']}")
                            
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
        self.save_stats()
        self.cap.release()
        self.hands.close()
        self.root.destroy()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedHandGestureDrawingApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()