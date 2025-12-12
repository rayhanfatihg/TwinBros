import pygame
import os

class AudioManager:
    def __init__(self, sound_dir):
        self.sound_dir = sound_dir
        self.tracks = []
        self.current_index = 0
        
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Load tracks
        if os.path.exists(sound_dir):
            for f in os.listdir(sound_dir):
                if f.lower().endswith('.mp3') or f.lower().endswith('.wav'):
                    self.tracks.append(os.path.join(sound_dir, f))
        
        if not self.tracks:
            print(f"[WARNING] No music files found in {sound_dir}")

    def play(self):
        if not self.tracks: return
        try:
            pygame.mixer.music.load(self.tracks[self.current_index])
            pygame.mixer.music.play(-1) # Loop indefinitely
        except Exception as e:
            print(f"[ERROR] Failed to play music: {e}")

    def stop(self):
        pygame.mixer.music.stop()

    def next_track(self):
        if not self.tracks: return
        self.current_index = (self.current_index + 1) % len(self.tracks)

    def prev_track(self):
        if not self.tracks: return
        self.current_index = (self.current_index - 1) % len(self.tracks)

    def get_current_track_name(self):
        if not self.tracks: return "No Music Found"
        return os.path.basename(self.tracks[self.current_index])
