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
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"session_{timestamp}.mp4"
        path = os.path.join(self.output_dir, filename)
        
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = cv2.VideoWriter(path, fourcc, fps, (width, height))
        self.is_recording = True
        self.current_video_path = path
        print(f"[INFO] Recording started: {path}")
        return path

    def write(self, frame):
        if self.is_recording and self.writer is not None:
            self.writer.write(frame)

    def stop(self, audio_path=None):
        if self.is_recording:
            self.writer.release()
            self.writer = None
            self.is_recording = False
            
            final_path = self.current_video_path
            
            # If audio path is provided, merge it
            if audio_path and os.path.exists(audio_path):
                print(f"[INFO] Merging audio: {audio_path}")
                try:
                    # Lazy import to avoid startup lag
                    from moviepy import VideoFileClip, AudioFileClip
                    
                    video_clip = VideoFileClip(self.current_video_path)
                    audio_clip = AudioFileClip(audio_path)
                    
                    # Loop audio if shorter, or trim if longer
                    if audio_clip.duration < video_clip.duration:
                        # Simple loop logic or just let it end? 
                        # Usually music is longer. If shorter, let's strictly valid clip.
                        pass 
                    
                    # Trim audio to match video duration
                    audio_clip = audio_clip.subclipped(0, video_clip.duration)
                    
                    final_clip = video_clip.with_audio(audio_clip)
                    
                    # Rename original to temp
                    base, ext = os.path.splitext(self.current_video_path)
                    temp_path = f"{base}_temp{ext}"
                    
                    # Close the video clip reader so we can rename/delete
                    # But VideoFileClip holds the file open.
                    # Instead, write to a NEW file, then delete old.
                    final_output_path = f"{base}_audio{ext}"
                    
                    final_clip.write_videofile(final_output_path, codec="libx264", audio_codec="aac", logger=None)
                    
                    # Close clips
                    video_clip.close()
                    audio_clip.close()
                    
                    # Cleanup: Remove original silent video, rename new one to original name?
                    # Or keep 'session_..._audio.mp4' as the result?
                    # Let's replace the original to keep filenames clean.
                    os.remove(self.current_video_path)
                    os.rename(final_output_path, self.current_video_path)
                    
                except Exception as e:
                    print(f"[ERROR] Failed to merge audio: {e}")
            
            print(f"[INFO] Recording stopped: {final_path}")
            return final_path
        return None
