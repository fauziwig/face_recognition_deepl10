import cv2
import time
import threading
import tkinter as tk
from tkinter import messagebox
from mtcnn import MTCNN

# Load the MTCNN face detector
face_detector = MTCNN()
camera = cv2.VideoCapture(1)

# Global variables for threading
running = False

def face_detection(frame):
    # Convert the frame to RGB as MTCNN expects RGB images
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = face_detector.detect_faces(rgb_frame)
    return faces

def drawer_box(frame):
    faces = face_detection(frame)
    for face in faces:
        x, y, w, h = face['box']
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 4)

def close_window():
    global running
    running = False
    camera.release()
    cv2.destroyAllWindows()
    root.quit()

def video_loop():
    global running
    prev_frame_time = 0
    new_frame_time = 0

    while running:
        ret, frame = camera.read()
        if not ret:
            break

        new_frame_time = time.time()

        # Calculate FPS
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time

        # Convert the FPS to an integer
        fps = int(fps)

        # Draw the bounding box around faces
        drawer_box(frame)

        # Put FPS text on the frame
        cv2.putText(frame, f"FPS: {fps}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Display the frame
        cv2.imshow("Face Detection Wiguna", frame)

        # Check if 'b' key is pressed to go back to the control panel
        if cv2.waitKey(1) & 0xFF == ord('b'):
            back_to_main()
            break

        # Check if 'q' key is pressed to close the application
        if cv2.waitKey(1) & 0xFF == ord('q'):
            close_window()
            break

def start_detection():
    global running
    if not running:
        running = True
        thread = threading.Thread(target=video_loop)
        thread.start()
    else:
        messagebox.showwarning("Warning", "Detection is already running!")

def stop_detection():
    global running
    if running:
        running = False
    else:
        messagebox.showwarning("Warning", "Detection is not running!")

def open_detection_window():
    main_frame.pack_forget()
    detection_frame.pack()

def back_to_main():
    global running
    running = False
    cv2.destroyAllWindows()
    detection_frame.pack_forget()
    main_frame.pack()

# Set up the main GUI
root = tk.Tk()
root.title("Face Detection Control Panel")

main_frame = tk.Frame(root)
main_frame.pack()

start_detection_button = tk.Button(main_frame, text="Open Face Detection", command=open_detection_window)
start_detection_button.pack(pady=10)

close_main_button = tk.Button(main_frame, text="Close", command=close_window)
close_main_button.pack(pady=10)

# Set up the detection GUI
detection_frame = tk.Frame(root)

start_button = tk.Button(detection_frame, text="Start Detection", command=start_detection)
start_button.pack(pady=10)

stop_button = tk.Button(detection_frame, text="Stop Detection", command=stop_detection)
stop_button.pack(pady=10)

back_button = tk.Button(detection_frame, text="Back", command=back_to_main)
back_button.pack(pady=10)

close_button = tk.Button(detection_frame, text="Close", command=close_window)
close_button.pack(pady=10)

root.protocol("WM_DELETE_WINDOW", close_window)

root.mainloop()
