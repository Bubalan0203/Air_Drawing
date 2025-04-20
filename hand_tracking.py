
# File: hand_tracking.py
import mediapipe as mp

class HandDetector:
    def __init__(self):
        self.hands = mp.solutions.hands.Hands(max_num_hands=1)

    def detect_hand(self, image):
        result = self.hands.process(image)
        if result.multi_hand_landmarks:
            return result.multi_hand_landmarks[0]
        return None
