import cv2
import numpy as np
import time
import os
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
    print("[INFO] Tekan 's' untuk mulai sesi, 'q' untuk keluar.")

    SESSION_DURATION = 15  # seconds
    POSE_INTERVAL = 3      # seconds
    
    # Pre-load iconic images mapping
    # Assuming iconic images are in data/iconic_images and filenames match the pose names (without _personX)
    iconic_img_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "iconic_images")
    
    while True:
        frame, keypoints = cam.get_frame()
        if frame is None:
            print("[ERROR] Kamera tidak tersedia.")
            break

        # Draw YOLO keypoints
        if keypoints is not None:
            for person in keypoints:
                for (x, y, conf) in person:
                    if conf > 0.5:
                        cv2.circle(frame, (int(x), int(y)), 3, (0, 255, 0), -1)

        ui.overlay_text(frame, "Press 'S' to Start Session | 'Q' to Quit", (20, 460))
        cv2.imshow("TwinBros", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        
        elif key == ord('s'):
            print("[INFO] Starting session...")
            start_time = time.time()
            next_capture_time = start_time + POSE_INTERVAL
            
            while (time.time() - start_time) < SESSION_DURATION:
                frame, keypoints = cam.get_frame()
                if frame is None: break
                
                remaining_time = int(SESSION_DURATION - (time.time() - start_time))
                ui.overlay_text(frame, f"Session Time: {remaining_time}s", (20, 50), color=(0, 255, 255))
                
                # Show countdown to next capture
                time_to_capture = next_capture_time - time.time()
                if time_to_capture > 0:
                     ui.overlay_text(frame, f"Next Pose in: {int(time_to_capture)+1}", (20, 100), color=(0, 0, 255))

                # Draw keypoints
                if keypoints is not None:
                    for person in keypoints:
                        for (x, y, conf) in person:
                            if conf > 0.5:
                                cv2.circle(frame, (int(x), int(y)), 3, (0, 255, 0), -1)

                cv2.imshow("TwinBros", frame)
                cv2.waitKey(1)
                
                if time.time() >= next_capture_time:
                    # Capture!
                    trans.flash_effect()
                    print("[INFO] Capturing pose...")
                    
                    if keypoints and len(keypoints) > 0:
                        person = keypoints[0]
                        coords = np.array(person)[:, :2]
                        norm_pose = detector.normalize_pose(coords)
                        
                        best_name, best_score = matcher.match(norm_pose)
                        print(f"[OK] Match found: {best_name} (Score: {best_score:.2f})")
                        
                        # Find iconic image
                        # best_name example: "walter_pinkma_person1.json" -> "walter_pinkma"
                        base_name = best_name.split("_person")[0]
                        
                        # Search for image with this base_name in iconic_images
                        image_path = None
                        for f in os.listdir(iconic_img_dir):
                            if f.startswith(base_name):
                                image_path = os.path.join(iconic_img_dir, f)
                                break
                        
                        ui.show_match_result(image_path, base_name, best_score, duration=2000)
                        
                        # Adjust next capture time to account for the display duration
                        # We want to maintain the rhythm, but we just spent 2s showing the result.
                        # So we reset the next capture time relative to NOW.
                        next_capture_time = time.time() + POSE_INTERVAL
                        
                    else:
                        print("[INFO] Tidak ada pose terdeteksi.")
                        ui.transition_message("No Pose Detected", 1000)
                        next_capture_time = time.time() + POSE_INTERVAL

            print("[INFO] Session ended.")
            ui.transition_message("Session Ended", 2000)

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


