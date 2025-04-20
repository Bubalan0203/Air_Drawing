
# File: ui_elements.py
import cv2

class UIManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.buttons = [
            {'x': 10, 'y': 10, 'w': 40, 'h': 40, 'color': (0, 0, 255), 'action': 'color_red'},
            {'x': 60, 'y': 10, 'w': 40, 'h': 40, 'color': (0, 255, 0), 'action': 'color_green'},
            {'x': 110, 'y': 10, 'w': 40, 'h': 40, 'color': (255, 0, 0), 'action': 'color_blue'},
            {'x': 160, 'y': 10, 'w': 40, 'h': 40, 'color': (255, 255, 0), 'action': 'color_yellow'},
            {'x': 210, 'y': 10, 'w': 60, 'h': 40, 'label': 'CLEAR', 'action': 'clear'},
            {'x': 280, 'y': 10, 'w': 60, 'h': 40, 'label': 'SAVE', 'action': 'save'},
            {'x': 350, 'y': 10, 'w': 60, 'h': 40, 'label': 'LOAD', 'action': 'load'},
            {'x': 420, 'y': 10, 'w': 80, 'h': 40, 'label': 'THEME', 'action': 'theme'},
        ]

    def draw_buttons(self, frame, current_color, theme):
        for btn in self.buttons:
            x, y, w, h = btn['x'], btn['y'], btn['w'], btn['h']
            if 'color' in btn['action']:
                cv2.rectangle(frame, (x, y), (x + w, y + h), btn['color'], -1)
                if btn['color'] == current_color:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
            else:
                bg_color = (50, 50, 50) if theme == 'dark' else (220, 220, 220)
                text_color = (255, 255, 255) if theme == 'dark' else (0, 0, 0)
                cv2.rectangle(frame, (x, y), (x + w, y + h), bg_color, -1)
                cv2.putText(frame, btn['label'], (x + 5, y + 28), cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2)
        return frame

    def check_hover(self, point):
        if point is None:
            return False
        x, y = point
        for btn in self.buttons:
            bx, by, bw, bh = btn['x'], btn['y'], btn['w'], btn['h']
            if bx < x < bx + bw and by < y < by + bh:
                return True
        return False

    def handle_buttons(self, point):
        if point is None:
            return None
        x, y = point
        for btn in self.buttons:
            if btn['x'] < x < btn['x'] + btn['w'] and btn['y'] < y < btn['y'] + btn['h']:
                return btn['action']
        return None

    def toggle_theme(self, theme):
        pass  # placeholder, as theme toggling is handled via draw_buttons
