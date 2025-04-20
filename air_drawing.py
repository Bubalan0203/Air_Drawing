import cv2
import mediapipe as mp
import numpy as np
import time
import speech_recognition as sr
import threading

# Initialize mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Setup webcam
cap = cv2.VideoCapture(0)

# Drawing setup
canvas_width, canvas_height = 640, 480
canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)
prev_x, prev_y = 0, 0
thickness = 5

# Colors and UI buttons
colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 255, 0)]
color_index = 0
color = colors[color_index]

button_height = 40
button_width = 40
button_margin = 10
buttons = []
for i, col in enumerate(colors):
    x1 = button_margin + i * (button_width + button_margin)
    y1 = button_margin
    buttons.append({'x1': x1, 'y1': y1, 'x2': x1 + button_width, 'y2': y1 + button_height, 'color': col})

# Clear button
clear_button = {'x1': 500, 'y1': 10, 'x2': 620, 'y2': 50, 'label': 'CLEAR'}

# Undo/Redo stack
drawing_history = []  # Stack to keep the history of the canvas
history_index = -1  # Points to the most recent canvas state

# Brush Type
brush_type = 'Solid'

# Initialize Speech Recognition
recognizer = sr.Recognizer()

# Function for voice commands
def listen_for_voice_commands():
    global color, color_index, canvas, prev_x, prev_y, history_index
    while True:
        with sr.Microphone() as source:
            print("Listening for commands...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

            try:
                action = recognizer.recognize_google(audio).lower()
                print(f"Voice command: {action}")
                
                if action:  # Ensure 'action' is not None
                    if action.startswith('color_'):
                        # Handle color change based on voice command
                        color_index = int(action.split('_')[1])  # Extract color index
                        color = colors[color_index]
                        print(f"Color changed to {color}")
                    elif action == 'undo':
                        # Handle undo command
                        if history_index > 0:
                            history_index -= 1
                            canvas = drawing_history[history_index]
                            print("Undo executed")
                    elif action == 'redo':
                        # Handle redo command
                        if history_index < len(drawing_history) - 1:
                            history_index += 1
                            canvas = drawing_history[history_index]
                            print("Redo executed")
                    elif action == 'save':
                        # Handle save command
                        filename = f"drawing_{int(time.time())}.png"
                        cv2.imwrite(filename, canvas)
                        print(f"Saved drawing as {filename}")
                    elif action == 'clear':
                        # Handle clear command
                        canvas[:] = 0
                        prev_x, prev_y = 0, 0
                        print("Canvas cleared")
                    elif action == 'toggle_theme':
                        # Handle theme toggle command
                        print("Theme toggled")

            except Exception as e:
                print(f"Error: {str(e)}")

# Start listening for voice commands in a separate thread
voice_thread = threading.Thread(target=listen_for_voice_commands, daemon=True)
voice_thread.start()

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (canvas_width, canvas_height))
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    h, w, _ = frame.shape

    index_finger_tip = None

    if result.multi_hand_landmarks:
        hand_landmarks = result.multi_hand_landmarks[0]
        lm = hand_landmarks.landmark
        index_finger_tip = (int(lm[8].x * w), int(lm[8].y * h))

        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Draw color buttons
    for i, btn in enumerate(buttons):
        x1, y1, x2, y2 = btn['x1'], btn['y1'], btn['x2'], btn['y2']
        cv2.rectangle(frame, (x1, y1), (x2, y2), btn['color'], -1)
        if color_index == i:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)

    # Draw clear button
    cv2.rectangle(frame, (clear_button['x1'], clear_button['y1']),
                  (clear_button['x2'], clear_button['y2']), (200, 200, 200), -1)
    cv2.putText(frame, clear_button['label'],
                (clear_button['x1'] + 5, clear_button['y1'] + 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    if index_finger_tip:
        ix, iy = index_finger_tip

        # Check color button click
        for i, btn in enumerate(buttons):
            if btn['x1'] < ix < btn['x2'] and btn['y1'] < iy < btn['y2']:
                color_index = i
                color = colors[i]
                prev_x, prev_y = 0, 0  # reset so drawing doesn't jump
                break

        # Check clear button click
        if clear_button['x1'] < ix < clear_button['x2'] and clear_button['y1'] < iy < clear_button['y2']:
            canvas[:] = 0
            prev_x, prev_y = 0, 0
            cv2.putText(frame, 'Canvas Cleared', (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        # Skip drawing if finger is on a button
        over_button = any(btn['x1'] < ix < btn['x2'] and btn['y1'] < iy < btn['y2'] for btn in buttons) or \
                      (clear_button['x1'] < ix < clear_button['x2'] and clear_button['y1'] < iy < clear_button['y2'])

        if not over_button:
            if prev_x == 0 and prev_y == 0:
                prev_x, prev_y = ix, iy
            cv2.line(canvas, (prev_x, prev_y), (ix, iy), color, thickness)
            prev_x, prev_y = ix, iy
        else:
            prev_x, prev_y = 0, 0
    else:
        prev_x, prev_y = 0, 0

    # Display the result
    blended = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)
    cv2.imshow("Air Drawing", blended)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('s'):
        filename = f"drawing_{int(time.time())}.png"
        cv2.imwrite(filename, canvas)
        print(f"Saved drawing as {filename}")

cap.release()
cv2.destroyAllWindows()
