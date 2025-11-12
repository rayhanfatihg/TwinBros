import os
import json
import numpy as np

# Path dasar project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFERENCE_DIR = os.path.join(BASE_DIR, "data", "reference_poses")

def load_reference_poses():
    """Membaca semua file JSON pose referensi."""
    references = {}
    for file in os.listdir(REFERENCE_DIR):
        if file.endswith(".json"):
            path = os.path.join(REFERENCE_DIR, file)
            with open(path, "r") as f:
                data = np.array(json.load(f))
                references[file] = data
    return references


def cosine_similarity(a, b):
    """Hitung kesamaan antara dua pose dengan cosine similarity."""
    # Flatten semua titik (x,y)
    a = a.flatten()
    b = b.flatten()
    # Normalisasi
    a /= np.linalg.norm(a) + 1e-8
    b /= np.linalg.norm(b) + 1e-8
    return np.dot(a, b)


def match_pose(user_pose, reference_poses):
    """
    Bandingkan pose user dengan semua referensi.
    Return: nama file referensi dengan skor tertinggi + nilai skor.
    """
    best_match = None
    best_score = -1

    for name, ref_pose in reference_poses.items():
        # Jika jumlah titik berbeda, sesuaikan panjang minimum
        n = min(len(user_pose), len(ref_pose))
        score = cosine_similarity(np.array(user_pose[:n]), ref_pose[:n])
        if score > best_score:
            best_match = name
            best_score = score

    return best_match, best_score


if __name__ == "__main__":
    # Contoh penggunaan (testing manual)
    import random

    refs = load_reference_poses()
    print(f"[INFO] Loaded {len(refs)} reference poses.")

    # Simulasi pose user random (misal 17 keypoints)
    user_pose = np.random.rand(17, 2)

    match_name, score = match_pose(user_pose, refs)
    print(f"[MATCH] Paling mirip dengan: {match_name} (skor: {score:.4f})")
