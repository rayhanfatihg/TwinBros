import cv2
import numpy as np
from ultralytics import YOLO

class PoseDetector:
    def __init__(self, model_path="yolo11n-pose.pt", conf=0.5):
        self.model = YOLO(model_path)
        self.conf = conf

    def normalize_pose(self, keypoints):
        coords = keypoints[:, :2]  # hanya ambil x, y
        coords -= coords.mean(axis=0)  # pusatkan ke tengah
        norm = np.linalg.norm(coords)
        if norm > 0:
            coords /= norm
        return coords

    def detect_poses(self, frame):
        results = self.model(frame, conf=self.conf)
        poses = []

        for result in results:
            if result.keypoints is not None and len(result.keypoints) > 0:
                for kp in result.keypoints:
                    coords = kp.xy.cpu().numpy().squeeze()
                    norm_pose = self.normalize_pose(coords)
                    poses.append(norm_pose)
        return poses

    def get_keypoints(self, frame):
        # Mirroring the logic from Camera class
        results = self.model.predict(source=frame, verbose=False)
        keypoints = None
        if len(results) > 0 and results[0].keypoints is not None:
            kps = results[0].keypoints
            xy = kps.xy.cpu().numpy()
            conf = kps.conf.cpu().numpy()
            keypoints = [list(zip(x[:, 0], x[:, 1], c)) for x, c in zip(xy, conf)]
        return keypoints

    def draw_poses(self, frame, results):
        annotated = frame.copy()
        for result in results:
            if result.keypoints is not None:
                annotated = result.plot()
        return annotated


if __name__ == "__main__":
    detector = PoseDetector()
    cap = cv2.VideoCapture(0)

    print("[INFO] Kamera aktif. Tekan 'q' untuk keluar.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = detector.model(frame)
        annotated = detector.draw_poses(frame, results)

        poses = detector.detect_poses(frame)
        cv2.putText(annotated, f"Detected poses: {len(poses)}",
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("Pose Detection - YOLO11", annotated)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
