import cv2
import numpy as np
from camera import Camera
from ui import UI
from transition import Transition
from pose_detection import PoseDetector
from pose_matching import PoseMatcher

def main():
    cam = Camera()
    ui = UI()
    trans = Transition(ui)

    detector = PoseDetector()          # load YOLO once
    matcher = PoseMatcher()            # load reference poses once

    print("=== TwinBros Pose Matching App ===")
    print("[INFO] Tekan 'c' untuk capture pose, 'q' untuk keluar.")

    while True:
        frame, keypoints = cam.get_frame()  # YOLO returns (annotated_frame, keypoints)
        if frame is None:
            print("[ERROR] Kamera tidak tersedia.")
            break

        # Draw YOLO keypoints manually if available
        if keypoints is not None:
            for person in keypoints:
                for (x, y, conf) in person:
                    if conf > 0.5:
                        cv2.circle(frame, (int(x), int(y)), 3, (0, 255, 0), -1)

        ui.overlay_text(frame, "Press 'C' to Capture | 'Q' to Quit", (20, 460))
        cv2.imshow("TwinBros", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

        elif key == ord('c'):
            trans.countdown(3, cam)
            trans.flash_effect()
            print("[INFO] Capturing pose...")

            # Use PoseDetector’s normalization logic directly
            if keypoints and len(keypoints) > 0:
                person = keypoints[0]  # assume first person
                coords = np.array(person)[:, :2]  # x, y
                norm_pose = detector.normalize_pose(coords)

                # Compare with references
                best_name, best_score = matcher.match(norm_pose)
                print(f"[OK] Match found: {best_name} (Score: {best_score:.2f})")

                ui.transition_message(f"Matched: {best_name}", 1500)
            else:
                print("[INFO] Tidak ada pose terdeteksi.")
                ui.transition_message("No Pose Detected", 1500)

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


