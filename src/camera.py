import cv2
from ultralytics import YOLO

class Camera:
    def __init__(self, width=640, height=480, model_path="yolov8n-pose.pt"):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # use CAP_DSHOW for Windows
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        if not self.cap.isOpened():
            raise RuntimeError("Camera not detected or already in use")

        self.model = YOLO(model_path)
        self.width = width
        self.height = height

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, None

        results = self.model.predict(source=frame, verbose=False)

        keypoints = None
        if len(results) > 0 and results[0].keypoints is not None:
            kps = results[0].keypoints
            xy = kps.xy.cpu().numpy()
            conf = kps.conf.cpu().numpy()
            keypoints = [list(zip(x[:, 0], x[:, 1], c)) for x, c in zip(xy, conf)]
            annotated = results[0].plot()
            return annotated, keypoints

        return frame, None

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