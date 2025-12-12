import cv2
import numpy as np
import time
import os
from camera import Camera
from ui import UI
from transition import Transition
from pose_detection import PoseDetector
from pose_matching import PoseMatcher
from audio import AudioManager
from video_recorder import VideoRecorder

def main():
    cam = Camera()
    ui = UI()
    trans = Transition(ui)

    detector = PoseDetector()          # load YOLO once
    matcher = PoseMatcher()            # load reference poses once
    
    # Initialize Audio and Video
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sound_dir = os.path.join(base_dir, "assets", "sounds")
    output_dir = os.path.join(base_dir, "output")
    
    audio_manager = AudioManager(sound_dir)
    video_recorder = VideoRecorder(output_dir)

    print("=== TwinBros Pose Matching App ===")
    print("[INFO] Tekan 's' untuk mulai sesi, 'q' untuk keluar.")
    print("[INFO] Gunakan Panah Kiri/Kanan (atau A/D) untuk memilih musik.")

    SESSION_DURATION = 15  # seconds
    POSE_INTERVAL = 3      # seconds
    
    # Pre-load iconic images mapping
    iconic_img_dir = os.path.join(base_dir, "data", "iconic_images")
    
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

        ui.overlay_text(frame, "Press 'S' to Start | 'Q' to Quit", (20, 460))
        ui.overlay_text(frame, f"Music (< A/D >): {audio_manager.get_current_track_name()}", (20, 430), scale=0.6)
        
        cv2.imshow("TwinBros", frame)

        key = cv2.waitKeyEx(1)
        if key == ord('q'):
            break
        
        # Arrow Keys (Windows) or A/D
        # Left Arrow: 2424832, Right Arrow: 2555904
        elif key == 2424832 or key == ord('a'): # Left
            audio_manager.prev_track()
        elif key == 2555904 or key == ord('d'): # Right
            audio_manager.next_track()
        
        elif key == ord('s'):
            print("[INFO] Starting session...")
            
            # Start Music and Recording
            audio_manager.play()
            video_path = video_recorder.start(frame.shape[1], frame.shape[0])
            
            start_time = time.time()
            next_capture_time = start_time + POSE_INTERVAL
            
            while (time.time() - start_time) < SESSION_DURATION:
                frame, keypoints = cam.get_frame()
                if frame is None: break
                
                # Record frame
                video_recorder.write(frame)
                
                remaining_time = int(SESSION_DURATION - (time.time() - start_time))
                ui.overlay_text(frame, f"Session Time: {remaining_time}s", (20, 50), color=(255, 255, 255))
                
                # Show countdown to next capture
                time_to_capture = next_capture_time - time.time()
                if time_to_capture > 0:
                     ui.overlay_text(frame, f"Next Pose in: {int(time_to_capture)+1}", (20, 100), color=(255, 255, 255))

                # Draw keypoints
                if keypoints is not None:
                    for person in keypoints:
                        for (x, y, conf) in person:
                            if conf > 0.5:
                                cv2.circle(frame, (int(x), int(y)), 3, (0, 255, 0), -1)

                cv2.imshow("TwinBros", frame)
                key = cv2.waitKey(1)
                
                if time.time() >= next_capture_time:
                    # Capture!
                    trans.flash_effect(video_recorder)
                    print("[INFO] Capturing pose...")
                    
                    if keypoints and len(keypoints) > 0:
                        person = keypoints[0]
                        coords = np.array(person)[:, :2]
                        norm_pose = detector.normalize_pose(coords)
                        
                        best_name, best_score = matcher.match(norm_pose)
                        print(f"[OK] Match found: {best_name} (Score: {best_score:.2f})")
                        
                        # Find iconic image
                        base_name = best_name.split("_person")[0]
                        image_path = None
                        for f in os.listdir(iconic_img_dir):
                            if f.startswith(base_name):
                                image_path = os.path.join(iconic_img_dir, f)
                                break
                        
                        # Pause recording briefly if we want to show the result in the video? 
                        # Or just show it on screen. The recorder captures frames from the loop.
                        # If show_match_result uses cv2.imshow and waitKey, it might NOT be recorded unless we explicitly write frames there.
                        # For now, let's keep the simple flow. The user sees the result, but the video might skip it or show it frozen if we don't handle it.
                        # Actually show_match_result blocks the loop with waitKey.
                        # To record the result overlay, we would need to modify show_match_result to return the image or handle recording internally.
                        # For now, let's accept that the result display is a "pause" in the session flow.
                        
                        ui.show_match_result(image_path, base_name, best_score, duration=2000, video_recorder=video_recorder)
                        
                        next_capture_time = time.time() + POSE_INTERVAL
                        
                    else:
                        print("[INFO] Tidak ada pose terdeteksi.")
                        ui.transition_message("No Pose Detected", 1000, video_recorder)
                        next_capture_time = time.time() + POSE_INTERVAL

            print("[INFO] Session ended.")
            
            # Stop Music and Recording
            audio_manager.stop()
            video_recorder.stop()
            
            ui.transition_message("Session Ended", 2000, video_recorder)
            
            # Drive Upload Message
            drive_link = "https://drive.google.com/drive/folders/1Knv2PaaFLN57YNlExWAAgRxrw-eAakg5?usp=sharing"
            print(f"\n[IMPORTANT] Video saved to: {video_path}")
            print(f"[IMPORTANT] Please upload the video to Google Drive: {drive_link}\n")
            
            # Show message on UI
            blank = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(blank, "Video Saved!", (200, 200), ui.font, 1, (255, 255, 255), 2)
            cv2.putText(blank, "Upload to Drive", (180, 250), ui.font, 0.8, (255, 255, 255), 1)
            cv2.imshow("TwinBros", blank)
            cv2.waitKey(3000)

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


