TwinBros

Twinning with your bros

Made by :

- Rayhan Fatih Gunawan
  
- Muhammad Nelwan Fakhri
  
- Raditya Erza Farandi

## 📝 Deskripsi Singkat

TwinBros adalah sebuah filter yang memungkinkan pengguna merekonstruksi momen ikonik dari pasangan karakter pop culture bersama teman (bros).
Nama “Twin” diambil dari istilah slang, yang berarti “match”, “mirroring each other”, atau “berpenampilan/bergaya sama dengan orang lain dalam cara yang fun dan kompak”. Istilah ini banyak digunakan di budaya internet untuk menunjukkan kebersamaan atau chemistry antar dua orang.

Cara kerjanya adalah pengguna cukup meniru pose dari sebuah iconic pop culture duo moment, kemudian filter akan mendeteksi pose kedua pengguna dan menyesuaikan visualnya (background, atribut, warna, dll.) agar menyerupai referensi aslinya, sehingga terlihat seperti recreation dari momen ikonik tersebut.

## 📁 Struktur Folder

twinbros/
│
├── data/
│   ├── reference_poses/        # Pose referensi duo ikonik (bisa .json, .jpg, .png)
│   ├── iconic_images/          # Gambar ikonik (Naruto-Sasuke, Mario-Luigi, dll)
│   └── samples/                # Contoh hasil foto user (opsional)
│
├── models/
│   ├── pose_estimation/        # Pretrained model (misal OpenPose / MediaPipe / YOLO-Pose)
│   └── face_detection/         # (opsional) deteksi wajah untuk tambahan efek
│
├── src/
│   ├── camera.py               # Capture video dari webcam
│   ├── pose_detection.py       # Deteksi pose dari frame kamera
│   ├── pose_matching.py        # Bandingkan pose user dengan referensi
│   ├── transition.py           # Efek transisi (fade, dissolve, zoom)
│   ├── ui.py                   # Antarmuka / display window
│   └── main.py                 # Entry point
│
├── assets/
│   ├── sounds/                 # Musik/efek suara transisi
│   └── fonts/                  # Font untuk overlay teks
│
├── output/
│   ├── logs/                   # Log hasil pengujian
│   └── results/                # Output akhir (video/foto transisi)
│
└── requirements.txt


