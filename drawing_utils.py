
# File: drawing_utils.py
import cv2
import numpy as np
import time
import os

class DrawingManager:
    def __init__(self, canvas):
        self.canvas = canvas
        self.prev_x, self.prev_y = 0, 0
        self.color = (0, 0, 255)
        self.thickness = 5
        self.history = []
        self.history_index = -1
        self.save_state()

    def save_state(self):
        self.history = self.history[:self.history_index + 1]
        self.history.append(self.canvas.copy())
        self.history_index += 1

    def draw(self, point):
        if point is None:
            return
        x, y = point
        if self.prev_x == 0 and self.prev_y == 0:
            self.prev_x, self.prev_y = x, y
        cv2.line(self.canvas, (self.prev_x, self.prev_y), (x, y), self.color, self.thickness)
        self.prev_x, self.prev_y = x, y
        self.save_state()

    def draw_shape(self, shape, point):
        if shape == 'circle':
            cv2.circle(self.canvas, point, 30, self.color, self.thickness)
            self.save_state()

    def reset_prev(self):
        self.prev_x, self.prev_y = 0, 0

    def set_color(self, color_name):
        color_dict = {
            'red': (0, 0, 255),
            'green': (0, 255, 0),
            'blue': (255, 0, 0),
            'yellow': (255, 255, 0)
        }
        self.color = color_dict.get(color_name, (0, 0, 255))

    def clear(self):
        self.canvas[:] = 0
        self.reset_prev()
        self.save_state()

    def save(self):
        filename = f'drawing_{int(time.time())}.png'
        cv2.imwrite(filename, self.canvas)

    def load(self):
        files = sorted([f for f in os.listdir('.') if f.startswith('drawing_') and f.endswith('.png')])
        if files:
            img = cv2.imread(files[-1])
            if img.shape == self.canvas.shape:
                self.canvas[:] = img
                self.save_state()

    def undo(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.canvas[:] = self.history[self.history_index]

    def redo(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.canvas[:] = self.history[self.history_index]

    def get_canvas(self):
        return self.canvas

    def get_color(self):
        return self.color



