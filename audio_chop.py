import os
import sys
import argparse

try:
    import librosa
    import soundfile as sf
except ImportError:
    print("[ERROR] Required libraries not found.")
    print("Please run: pip install librosa soundfile")
    sys.exit(1)

def chop_audio(file_path, start_sec, end_sec=None):
    if not os.path.exists(file_path):
        print(f"[ERROR] File not found: {file_path}")
        return

    try:
        print(f"[INFO] Loading: {file_path}")
        # Load audio with original sampling rate
        y, sr = librosa.load(file_path, sr=None)
        
        # Calculate start and end samples
        start_sample = int(start_sec * sr)
        
        if end_sec:
            end_sample = int(end_sec * sr)
            # Ensure end_sample doesn't exceed length
            end_sample = min(end_sample, len(y))
        else:
            end_sample = len(y)
            
        if start_sample >= end_sample:
            print("[ERROR] Start time must be less than end time (or total duration).")
            return

        # Chop
        y_chopped = y[start_sample:end_sample]
        
        # Save
        dir_name = os.path.dirname(file_path)
        base_name = os.path.basename(file_path)
        name, ext = os.path.splitext(base_name)
        
        # Default to .wav for output if input is mp3, as soundfile has limited mp3 write support
        output_ext = ".wav" 
        output_filename = f"{name}_chopped{output_ext}"
        output_path = os.path.join(dir_name, output_filename)
        
        sf.write(output_path, y_chopped, sr)
        print(f"[SUCCESS] Saved to: {output_path}")
        print(f"          Duration: {(end_sample - start_sample) / sr:.2f} seconds")

    except Exception as e:
        print(f"[ERROR] Failed to process file: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chop audio file using librosa.")
    parser.add_argument("file", help="Path to the audio file")
    parser.add_argument("--start", type=float, default=0, help="Start time in seconds (default: 0)")
    parser.add_argument("--end", type=float, help="End time in seconds (optional, defaults to end of file)")
    
    args = parser.parse_args()
    
    chop_audio(args.file, args.start, args.end)
