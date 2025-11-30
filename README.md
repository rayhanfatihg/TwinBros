# TwinBros - Aplikasi Pencocokan Pose

TwinBros adalah aplikasi interaktif yang mendeteksi pose pengguna menggunakan kamera dan mencocokkannya dengan pose referensi dari karakter ikonik. Aplikasi ini juga mendukung pemutaran musik latar dan perekaman sesi video secara otomatis.

## Struktur Proyek

Berikut adalah struktur folder dan file utama dalam proyek ini:

```
TwinBros/
├── assets/
│   └── sounds/            # Folder untuk file musik (.mp3)
├── data/
│   ├── iconic_images/     # Gambar karakter ikonik untuk ditampilkan saat match
│   └── reference_poses/   # File JSON berisi data pose referensi
├── output/                # Folder tempat video hasil rekaman disimpan
├── src/
│   ├── audio.py           # Modul manajemen musik (pygame)
│   ├── camera.py          # Modul akses kamera
│   ├── main.py            # Entry point utama aplikasi
│   ├── pose_detection.py  # Deteksi pose menggunakan YOLOv8
│   ├── pose_matching.py   # Logika pencocokan pose (Cosine Similarity)
│   ├── transition.py      # Efek transisi visual
│   ├── ui.py              # Tampilan antarmuka (Overlay teks/gambar)
│   └── video_recorder.py  # Modul perekaman video
├── audio_chop.py          # Script utilitas untuk memotong file audio
├── requirements.txt       # Daftar pustaka yang dibutuhkan
└── yolov8n-pose.pt        # Model YOLOv8 untuk deteksi pose
```

## Instalasi

Pastikan Anda telah menginstal Python (versi 3.8 atau lebih baru).

1.  **Clone atau Download** repositori ini.
2.  **Buat Virtual Environment** (Opsional tapi disarankan):
    ```bash
    python -m venv .venv
    # Windows:
    .\.venv\Scripts\activate
    # Mac/Linux:
    source .venv/bin/activate
    ```
3.  **Instal Dependensi**:
    Jalankan perintah berikut untuk menginstal semua pustaka yang diperlukan:
    ```bash
    pip install -r requirements.txt
    ```
    _Isi requirements.txt:_
    - `ultralytics` (YOLOv8)
    - `opencv-python`
    - `numpy`
    - `pygame`
    - `librosa`
    - `soundfile`

## Cara Menjalankan Aplikasi

### 1. Aplikasi Utama (Pose Matching)

Untuk menjalankan aplikasi utama:

```bash
python src/main.py
```

**Kontrol Aplikasi:**

- **`S`**: Mulai Sesi (Start Session). Sesi berlangsung selama 15 detik.
- **`Q`**: Keluar dari aplikasi.
- **Panah Kiri / `A`**: Lagu sebelumnya.
- **Panah Kanan / `D`**: Lagu berikutnya.

**Fitur:**

- Aplikasi akan mengambil pose setiap 3 detik.
- Jika pose cocok dengan referensi, gambar karakter ikonik akan muncul.
- Video sesi akan direkam otomatis dan disimpan di folder `output/`.
- Link Google Drive untuk upload video akan muncul di terminal setelah sesi selesai.

### 2. Utilitas Pemotong Audio (`audio_chop.py`)

Script ini digunakan untuk memotong bagian tertentu dari file audio (misalnya untuk mengambil reff lagu).

**Cara Penggunaan:**

```bash
python audio_chop.py "path/ke/file_audio.mp3" --start [detik_mulai] --end [detik_selesai]
```

**Contoh:**
Memotong lagu dari detik ke-30 sampai detik ke-45:

```bash
python audio_chop.py "assets/sounds/lagu_saya.mp3" --start 30 --end 45
```

File hasil potongan akan disimpan di folder yang sama dengan akhiran `_chopped.wav`.

---

**Catatan:**

- Pastikan file model `yolov8n-pose.pt` ada di direktori root.
- Pastikan folder `data/reference_poses` dan `data/iconic_images` terisi dengan data yang sesuai.
