import cv2
import numpy as np
from camera import Camera
from ui import UI
from transition import Transition
from pose_detection import PoseDetector
from pose_matching import match_pose

def main():
    cam = Camera()
    ui = UI()
    trans = Transition(ui)

    print("=== TwinBros Pose Matching App ===")
    print("[INFO] Tekan 'c' untuk capture pose, 'q' untuk keluar.")

    while True:
        frame, result = cam.get_frame()
        if frame is None:
            print("[ERROR] Kamera tidak tersedia.")
            break

        frame = ui.show_pose_overlay(frame, result.pose_landmarks, cam.mp_draw, cam.mp_pose)
        ui.overlay_text(frame, "Press 'C' to Capture | 'Q' to Quit", (20, 460))

        cv2.imshow("TwinBros", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

        elif key == ord('c'):
            trans.countdown(3)
            print("[INFO] Capturing pose...")

            pose_data = PoseDetector(result)
            matched = match_pose(pose_data)

            if matched:
                ui.transition_message(f"Matched: {matched['name']}", 1500)
                print(f"[OK] Match found: {matched['name']} (Score: {matched['score']:.2f})")
            else:
                ui.transition_message("No Match Found", 1500)
                print("[INFO] Tidak ada pose cocok ditemukan.")

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
