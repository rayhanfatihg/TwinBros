import cv2
import numpy as np

class UI:
    def __init__(self):
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def overlay_text(self, frame, text, pos=(20, 40), color=(0, 255, 0), scale=0.8):
        cv2.putText(frame, text, pos, self.font, scale, color, 2, cv2.LINE_AA)
        return frame

    def show_pose_overlay(self, frame, pose_landmarks, mp_draw, mp_pose):
        if pose_landmarks:
            mp_draw.draw_landmarks(frame, pose_landmarks, mp_pose.POSE_CONNECTIONS)
        return frame

    def transition_message(self, msg="Get Ready!", duration=1000):
        blank = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(blank, msg, (160, 240), self.font, 1.2, (255, 255, 255), 3, cv2.LINE_AA)
        cv2.imshow("TwinBros", blank)
        cv2.waitKey(duration)
