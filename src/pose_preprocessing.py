import os
import cv2
import json
import numpy as np
from ultralytics import YOLO

# === PATH SETUP ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONIC_DIR = os.path.join(BASE_DIR, "data", "iconic_images")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "reference_poses")
VISUAL_DIR = os.path.join(BASE_DIR, "data", "pose_visualizations")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(VISUAL_DIR, exist_ok=True)

# === YOLOv8 Pose Model ===
model = YOLO("yolov8n-pose.pt")  # bisa diganti ke yolov8m-pose.pt untuk akurasi lebih tinggi


def resize_and_pad(image, target_size=(640, 480)):
    """Resize gambar tanpa merusak rasio aslinya dan beri padding hitam."""
    h, w = image.shape[:2]
    target_w, target_h = target_size
    scale = min(target_w / w, target_h / h)
    new_w, new_h = int(w * scale), int(h * scale)
    resized = cv2.resize(image, (new_w, new_h))

    canvas = np.zeros((target_h, target_w, 3), dtype=np.uint8)
    x_offset = (target_w - new_w) // 2
    y_offset = (target_h - new_h) // 2
    canvas[y_offset:y_offset + new_h, x_offset:x_offset + new_w] = resized
    return canvas


def normalize_pose(keypoints):
    """Normalisasi koordinat pose agar konsisten antar gambar."""
    coords = np.array(keypoints)
    coords = coords[~np.all(coords == 0, axis=1)]  # hapus titik kosong

    if len(coords) == 0:
        return None

    coords -= coords.mean(axis=0)  # pusatkan
    body_height = coords[:, 1].max() - coords[:, 1].min()
    if body_height > 0:
        coords /= body_height

    norm = np.linalg.norm(coords)
    if norm != 0:
        coords /= norm

    return coords.tolist()


def extract_pose_from_image(image_path):
    """Deteksi semua pose manusia pada gambar dan kembalikan (poses, vis_image)."""
    image = cv2.imread(image_path)
    if image is None:
        print(f"[WARNING] Gagal membaca gambar: {image_path}")
        return [], None

    image = resize_and_pad(image)
    results = model(image, verbose=False)
    vis = image.copy()
    all_poses = []

    for result in results:
        if result.keypoints is None:
            continue

        for pid, keypoints in enumerate(result.keypoints.xy):
            keypoints = keypoints.cpu().numpy()
            norm_pose = normalize_pose(keypoints)

            if norm_pose is not None:
                all_poses.append(norm_pose)

                # Gambar landmark di visualisasi
                for x, y in keypoints:
                    if x > 0 and y > 0:
                        cv2.circle(vis, (int(x), int(y)), 3, (0, 255, 0), -1)
                cv2.putText(vis, f"P{pid+1}", (int(keypoints[0][0]), int(keypoints[0][1]) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)

    return all_poses, vis


def main():
    print("=== Pose Preprocessing (YOLOv8-Pose) ===")
    files = [f for f in os.listdir(ICONIC_DIR) if f.lower().endswith((".jpg", ".png", ".jpeg"))]

    if not files:
        print("[INFO] Tidak ada gambar di folder 'iconic_images/'.")
        return

    for file in files:
        path = os.path.join(ICONIC_DIR, file)
        poses, vis = extract_pose_from_image(path)

        if not poses:
            print(f"[WARNING] Tidak ada pose terdeteksi di {file}")
            continue

        # Simpan semua pose ke JSON
        for i, pose_data in enumerate(poses, start=1):
            out_path = os.path.join(OUTPUT_DIR, f"{os.path.splitext(file)[0]}_person{i}.json")
            with open(out_path, "w") as f:
                json.dump(pose_data, f, indent=2)
            print(f"[OK] Pose {i} disimpan: {out_path}")

        # Simpan visualisasi ke file
        if vis is not None:
            vis_path = os.path.join(VISUAL_DIR, f"{os.path.splitext(file)[0]}_vis.jpg")
            cv2.imwrite(vis_path, vis)
            print(f"[IMG] Visualisasi disimpan: {vis_path}")

        # (opsional) tampilkan sebentar
        cv2.imshow("Pose Preview", vis)
        cv2.waitKey(500)

    print("=== Selesai! Semua pose referensi & visualisasi telah diekstrak. ===")
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
