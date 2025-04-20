
# File: gesture_recognition.py
class GestureRecognizer:
    def get_index_tip(self, hand_landmarks, w, h):
        index = hand_landmarks.landmark[8]
        return (int(index.x * w), int(index.y * h))

    def detect_gesture(self, hand_landmarks, w, h):
        # Very simple: if thumb and index close = 'undo', middle & ring close = 'redo', else circle gesture
        landmarks = hand_landmarks.landmark
        index = (int(landmarks[8].x * w), int(landmarks[8].y * h))
        thumb = (int(landmarks[4].x * w), int(landmarks[4].y * h))
        middle = (int(landmarks[12].x * w), int(landmarks[12].y * h))
        ring = (int(landmarks[16].x * w), int(landmarks[16].y * h))

        dist_index_thumb = ((index[0] - thumb[0]) ** 2 + (index[1] - thumb[1]) ** 2) ** 0.5
        dist_mid_ring = ((middle[0] - ring[0]) ** 2 + (middle[1] - ring[1]) ** 2) ** 0.5

        if dist_index_thumb < 40:
            return 'undo'
        elif dist_mid_ring < 40:
            return 'redo'
        elif dist_index_thumb > 60:
            return 'circle'
        return 'none'

