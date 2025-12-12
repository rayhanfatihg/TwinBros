import cv2
import time
import numpy as np

class Transition:
    def __init__(self, ui):
        self.ui = ui

    def countdown(self, seconds, cam):
        """
        Countdown dengan update frame kamera (melalui self.ui.cam), overlay angka di atas live video.
        """
        while seconds > 0:
            frame, _ = cam.get_frame()  # Ambil frame terbaru dari kamera
            if frame is None:
                break

            self.ui.overlay_text(frame, f"Capturing in... {seconds}", (200, 200))
            cv2.imshow("TwinBros", frame)

            # Tunggu 1 detik sambil tetap update frame
            key = cv2.waitKey(1000) & 0xFF
            if key == ord('q'):
                break

            seconds -= 1

    def flash_effect(self, video_recorder=None):
        """
        Simulasi efek flash kamera dengan overlay putih singkat pada window video.
        """
        flash_img = 255 * np.ones((480, 640, 3), dtype=np.uint8)  # Ukuran image harus sesuai video stream!
        cv2.imshow("TwinBros", flash_img)
        
        if video_recorder:
            video_recorder.write(flash_img)
            
        cv2.waitKey(200)
        # Setelah efek, jangan destroy window agar stream tetap jalan!
        # cv2.destroyWindow("TwinBros")  # Jangan pakai ini!

