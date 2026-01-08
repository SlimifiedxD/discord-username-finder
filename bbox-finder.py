import time

import pyautogui as pag

print("Move mouse to top-left")
time.sleep(3)
x1, y1 = pag.position()

print("Move mouse to bottom-right")
time.sleep(3)
x2, y2 = pag.position()

print(f"Use this Bbox: ({x1}, {y1}, {x2}, {y2})")
