import os
import json
import numpy as np

class PoseMatcher:
    

    def __init__(self, base_dir=None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.reference_dir = os.path.join(base_dir, "data", "reference_poses")
        self.references = self._load_reference_poses()

    
    def _load_reference_poses(self):
        references = {}
        for file in os.listdir(self.reference_dir):
            if file.endswith(".json"):
                path = os.path.join(self.reference_dir, file)
                with open(path, "r") as f:
                    data = np.array(json.load(f))
                    references[file] = data
        print(f"[INFO] Loaded {len(references)} reference poses from {self.reference_dir}")
        return references

    def _cosine_similarity(self, a, b):
        """Hitung kesamaan antara dua pose dengan cosine similarity."""
        a = a.flatten()
        b = b.flatten()
        a /= np.linalg.norm(a) + 1e-8
        b /= np.linalg.norm(b) + 1e-8
        return np.dot(a, b)

   
    def match(self, user_pose):
        
        if not self.references:
            raise RuntimeError("Tidak ada pose referensi yang dimuat!")

        best_name, best_score = None, -1

        for name, ref_pose in self.references.items():
            n = min(len(user_pose), len(ref_pose))
            score = self._cosine_similarity(np.array(user_pose[:n]), ref_pose[:n])
            if score > best_score:
                best_name, best_score = name, score

        return best_name, best_score
