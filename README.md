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

# Proyek Deteksi Pose Ikonik (TwinBros)

Aplikasi ini menggunakan computer vision untuk mendeteksi pose dua orang secara real-time. Jika pose mereka cocok dengan pose duo ikonik (seperti Naruto-Sasuke atau Mario-Luigi) dari database, aplikasi akan memicu efek transisi keren dan menghasilkan foto/video ala ikon tersebut.

## 📂 Struktur Folder

```bash
twinbros/
├── data/
│   ├── reference_poses/    # Pose referensi duo ikonik (misal JSON, JPG)
│   ├── iconic_images/      # Gambar ikonik (Naruto-Sasuke, Mario-Luigi, dll)
│   ├── samples/            # Contoh hasil foto pengguna
│   └── models/
│       ├── pose_estimation/ # Model pretrained (MediaPipe / YOLO-Pose)
│       └── face_detection/  # (Opsional) model deteksi wajah
│
├── src/
│   ├── camera.py           # Menangani input kamera
│   ├── pose_detection.py   # Deteksi pose dua orang
│   ├── pose_matching.py    # Mencocokkan pose dengan pose referensi
│   ├── transition.py       # Efek transisi ke gambar ikonik
│   ├── ui.py               # Tampilan visual aplikasi
│   └── main.py             # Entry point aplikasi
│
├── assets/
│   ├── sounds/             # Efek suara transisi
│   └── fonts/              # Font untuk overlay teks
│
├── output/                 # (Bisa juga 'results') Output hasil foto/video akhir
├── logs/                   # Log hasil pengujian
├── results/                # (Bisa juga 'output') Output hasil foto/video akhir
│
└── README.md               # Dokumentasi proyek (file ini)


