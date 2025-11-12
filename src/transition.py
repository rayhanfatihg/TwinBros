import cv2
import time
import numpy as np

class Transition:
    def __init__(self, ui):
        self.ui = ui

    def countdown(self, seconds=3):
        """
        Countdown visual sebelum capture dimulai.
        """
        for i in range(seconds, 0, -1):
            self.ui.transition_message(f"Capturing in {i}...")
            time.sleep(1)

    def flash_effect(self):
        """
        Simulasi efek flash kamera.
        """
        flash = 255 * (1 - 0.1)
        img = (flash * np.ones((480, 640, 3), dtype=np.uint8))
        cv2.imshow("TwinBros", img)
        cv2.waitKey(200)
        cv2.destroyWindow("TwinBros")