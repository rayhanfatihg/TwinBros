import cv2

class Camera:
    def __init__(self, width=720, height=640):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # use CAP_DSHOW for Windows
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        if not self.cap.isOpened():
            raise RuntimeError("Camera not detected or already in use")

        self.width = width
        self.height = height

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None

        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)

        return frame

    def release(self):
        self.cap.release()

# ========== RUN LOOP ==========
if __name__ == "__main__":
    cam = Camera()
    while True:
        frame, kps = cam.get_frame()
        if frame is None:
            print("No frame received, exiting...")
            break

        cv2.imshow("YOLOv8 Pose Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

