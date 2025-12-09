
import streamlit as st
import cv2
import numpy as np
import time
import os
from src.camera import Camera
from src.pose_detection import PoseDetector
from src.pose_matching import PoseMatcher
from src.audio import AudioManager
from src.video_recorder import VideoRecorder

st.set_page_config(page_title="TwinBros Pose Matching", layout="wide")

# Cached Resources to prevent reloading/locking on rerun
@st.cache_resource
def get_camera():
    return Camera()

def get_detector():
    return PoseDetector()

@st.cache_resource
def get_matcher():
    return PoseMatcher()

@st.cache_resource
def get_audio_manager(sound_dir):
    return AudioManager(sound_dir)

def main():
    st.title("TwinBros Pose Matching")

    # Initialize Sidebar and Settings
    st.sidebar.title("Settings")
    
    # Music Selection
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sound_dir = os.path.join(base_dir, "assets", "sounds")
    
    # Ensure sound directory exists
    if not os.path.exists(sound_dir):
        os.makedirs(sound_dir)

    music_files = [f for f in os.listdir(sound_dir) if f.endswith('.mp3') or f.endswith('.wav')]
    # Use session state to persist music selection if needed, but selectbox does it automatically via 'value' if mapped
    # For now, standard selectbox is fine, but changing it triggers rerun.
    selected_music = st.sidebar.selectbox("Select Music", ["None"] + music_files)

    session_duration = st.sidebar.slider("Session Duration (s)", 10, 60, 15)
    pose_interval = st.sidebar.slider("Pose Interval (s)", 1, 10, 3)
    
    run_camera = st.sidebar.checkbox("Run Camera", value=False)
    
    if st.sidebar.button("Reset Cache (Fix Camera)"):
        st.cache_resource.clear()
        st.rerun()

    # Placeholders for UI
    col1, col2 = st.columns(2)
    with col1:
        time_metric = st.empty()
    with col2:
        next_pose_metric = st.empty()
        
    video_placeholder = st.empty()
    status_placeholder = st.empty()

    # Session State for Logic
    if "session_active" not in st.session_state:
        st.session_state.session_active = False
    if "start_time" not in st.session_state:
        st.session_state.start_time = 0
    if "next_capture_time" not in st.session_state:
        st.session_state.next_capture_time = 0
    if "match_display_until" not in st.session_state:
        st.session_state.match_display_until = 0
    if "last_match_image" not in st.session_state:
        st.session_state.last_match_image = None
    if "final_video_path" not in st.session_state:
        st.session_state.final_video_path = None
    
    # Video Recorder is lightweight (just logic), but the file handle in `writer` needs care.
    # We will instantiate it locally. If session interrupts, we might lose close. 
    # But usually VideoRecorder creates a new file on .start().
    output_dir = os.path.join(base_dir, "output")
    video_recorder = VideoRecorder(output_dir)

    # Helper objects
    if run_camera:
        # Load resources (cached where appropriate)
        try:
            cam = get_camera()
            # Detector is NOT cached to avoid 'AttributeError: bn'
            detector = get_detector()
            matcher = get_matcher()
            # Audio Manager depends on sound_dir.
            audio_manager = get_audio_manager(sound_dir)
        except Exception as e:
            st.error(f"Error loading resources: {e}")
            st.stop()
            
        # Update Audio Manager track
        if selected_music != "None":
             try:
                idx = audio_manager.tracks.index(os.path.join(sound_dir, selected_music))
                if audio_manager.current_index != idx:
                    audio_manager.current_index = idx
             except ValueError:
                pass
        
        iconic_img_dir = os.path.join(base_dir, "data", "iconic_images")

        # Start Button
        if not st.session_state.session_active:
            if st.button("Start Session"):
                st.session_state.session_active = True
                st.session_state.start_time = time.time()
                st.session_state.next_capture_time = st.session_state.start_time + pose_interval
                
                # Start Audio
                if selected_music != "None":
                    audio_manager.play()
                
                # Start Recorder
                frame = cam.get_frame()
                if frame is not None:
                    st.session_state.final_video_path = video_recorder.start(frame.shape[1], frame.shape[0])
                else:
                    st.error("Camera frame error.")
                    st.session_state.session_active = False
        else:
            if st.button("Stop Session"):
                st.session_state.session_active = False
                audio_manager.stop()
                # Recorder stop handled below or by new instance not being started.
                st.rerun()

        # Check for broken state (Session Active but Recorder is new/not started)
        # We can't easily check if `video_recorder` is "recording" a specific file from previous run.
        # So we might need to put video_recorder in cache too if we want it to survive reruns.
        # But VideoWriter isn't pickleable. 
        # For now, let's just warn correct usage: "Don't change settings during session".
        
        st.toast("Camera Running...", icon="📷")
        
        # We need to handle the case where session WAS active, but we just reran.
        # The local `video_recorder` is fresh. `is_recording` is False.
        # The user won't get a video for the full session if they interrupted it.
        # That is acceptable for V1.
        
        try:
            while run_camera:
                frame = cam.get_frame()
                if frame is None:
                    st.error("Failed to capture frame.")
                    break
                
                # Detect poses separately
                keypoints = detector.get_keypoints(frame)

                current_time = time.time()
                display_frame = frame.copy()

                # Session Logic
                if st.session_state.session_active:
                    # If we just reran and lost the recorder, we should probably warn or try to restart (new file)?
                    # `video_recorder` here is new. `is_recording` is False.
                    if not video_recorder.is_recording:
                         # We lost the handle. 
                         # Option A: Cancel session.
                         # st.session_state.session_active = False
                         # st.warning("Session interrupted by reload. Video stopped.")
                         # Option B: Just continue without recording?
                         # Option C: Start NEW recording?
                         pass # For now, we just lose the recording capability for the rest of the session if rerun happens.

                    elapsed = current_time - st.session_state.start_time
                    remaining = session_duration - elapsed

                    if remaining <= 0:
                        # End Session
                        st.session_state.session_active = False
                        audio_manager.stop()
                        
                        # Get audio path
                        audio_path = None
                        if selected_music != "None":
                            audio_path = os.path.join(sound_dir, selected_music)
                            
                        st.info("Processing video with audio...")
                        video_recorder.stop(audio_path=audio_path)
                        st.success(f"Session Finished!")
                        if st.session_state.final_video_path:
                             status_placeholder.info(f"Video saved to: {st.session_state.final_video_path}")
                        st.balloons()
                        # Allow break to refresh UI?
                        # break 
                    
                    # Logic continues...
                    # REMOVED: cv2.putText(display_frame, f"Time: {int(remaining)}s", (20, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 255), 2)
                    time_metric.metric("Session Time Left", f"{int(remaining)}s")

                    if current_time < st.session_state.match_display_until:
                        if st.session_state.last_match_image is not None:
                            match_img = cv2.resize(st.session_state.last_match_image, (display_frame.shape[1], display_frame.shape[0]))
                            display_frame = match_img
                    else:
                        time_to_capture = st.session_state.next_capture_time - current_time
                        if time_to_capture > 0:
                             # REMOVED: cv2.putText(display_frame, f"Next Pose: {int(time_to_capture)+1}", (20, 100), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
                             next_pose_metric.metric("Next Pose In", f"{int(time_to_capture)+1}s")
                        else:
                             next_pose_metric.metric("Next Pose In", "NOW!")
                        
                        if current_time >= st.session_state.next_capture_time:
                            # Flash Effect
                            flash_frame = 255 * np.ones_like(frame, dtype=np.uint8)
                            if st.session_state.session_active and video_recorder.is_recording:
                                video_recorder.write(flash_frame)
                            video_placeholder.image(flash_frame, channels="BGR")
                            time.sleep(0.2)
                            
                            if keypoints and len(keypoints) > 0:
                                person = keypoints[0]
                                coords = np.array(person)[:, :2]
                                norm_pose = detector.normalize_pose(coords)
                                best_name, best_score = matcher.match(norm_pose)
                                
                                base_name = best_name.split("_person")[0]
                                image_path = None
                                for f in os.listdir(iconic_img_dir):
                                    if f.startswith(base_name):
                                        image_path = os.path.join(iconic_img_dir, f)
                                        break
                                
                                if image_path and os.path.exists(image_path):
                                    img_overlay = cv2.imread(image_path)
                                    # Fix: Resize to match camera frame size
                                    img_overlay = cv2.resize(img_overlay, (frame.shape[1], frame.shape[0]))
                                else:
                                    img_overlay = np.zeros_like(frame)
                                    cv2.putText(img_overlay, "Image Not Found", (50, 240), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,255), 2)
                                
                                cv2.putText(img_overlay, f"{base_name} ({best_score:.2f})", (20, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
                                st.session_state.last_match_image = img_overlay
                                st.session_state.match_display_until = current_time + 2
                                display_frame = img_overlay
                            else:
                                st.toast("No Pose Detected!")
                            
                            st.session_state.next_capture_time = current_time + pose_interval + 2

                else:
                    cv2.putText(display_frame, "Press Start Session", (20, 460), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

                # Draw Keypoints (only in Standby mode)
                if not st.session_state.session_active:
                    if keypoints is not None:
                         for person in keypoints:
                            for (x, y, conf) in person:
                                if conf > 0.5:
                                    cv2.circle(display_frame, (int(x), int(y)), 3, (0, 255, 0), -1)

                # Record
                if st.session_state.session_active and video_recorder.is_recording:
                    video_recorder.write(display_frame)

                display_frame_rgb = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
                video_placeholder.image(display_frame_rgb, channels="RGB")
                time.sleep(0.01) # Slightly faster loop
        
        finally:
            # Cleanup if break
            if video_recorder.is_recording:
                video_recorder.stop()
            # Note: We do NOT release cam here because we want to reuse it!
            # But if the user unchecked "Run Camera", we loop exits. 
            pass

    else:
        st.info("Check 'Run Camera' in the sidebar to start.")
        # If camera was running before, we might want to release it?
        # But st.cache_resource keeps it alive.
        # If we really want to stop the light, we need to clear cache or add release logic.
        # For now, light stays on until cache clear or script kill. That's a known trade-off of cached camera.
        pass

if __name__ == "__main__":
    main()
