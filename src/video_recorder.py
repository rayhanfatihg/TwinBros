import cv2
import os
import time

class VideoRecorder:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        self.writer = None
        self.is_recording = False

    def start(self, width, height, fps=20.0):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"session_{timestamp}.avi"
        path = os.path.join(self.output_dir, filename)
        
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.writer = cv2.VideoWriter(path, fourcc, fps, (width, height))
        self.is_recording = True
        print(f"[INFO] Recording started: {path}")
        return path

    def write(self, frame):
        if self.is_recording and self.writer is not None:
            self.writer.write(frame)

    def stop(self):
        if self.is_recording:
            self.writer.release()
            self.writer = None
            self.is_recording = False
            print("[INFO] Recording stopped.")
