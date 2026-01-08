import itertools as itt
import platform
import random
import string
import time

import psutil as ps
import pyautogui as pag
import pywinctl as pwc
from PIL import ImageGrab

discord_pids = []


def find_discord_process():
    global discord_pid
    for proc in ps.process_iter(attrs=["pid", "name"]):
        name = proc.info["name"]
        if name is None:
            continue
        if "discord" not in name.lower():
            continue
        discord_pids.append(proc.info["pid"])


while len(discord_pids) == 0:
    find_discord_process()
    time.sleep(1)

IS_MAC = platform.system() == "Darwin"
SUPER_KEY = "command" if IS_MAC else "win"
CHARACTER_POOL = string.ascii_letters + string.digits + "_" + "."
TARGET_USERNAME_LENGTH = 3


def handle_name(name: str):
    pag.click(822, 512)
    # shit goes too fast if this is not >= 0.2
    time.sleep(0.2)
    pag.hotkey(SUPER_KEY if IS_MAC else "ctrl", "a")
    pag.press("backspace")
    pag.write(name)
    pag.press("tab", presses=2)
    # hand-picked box coordinates for username confirmation screen
    screenshot = ImageGrab.grab(bbox=(636, 535, 1030, 567))
    screenshot = screenshot.convert("RGB")
    red_pixels = 0
    green_pixels = 0
    for pixel in screenshot.get_flattened_data():
        assert isinstance(pixel, tuple)
        r, g, b = pixel
        if r > 100 and r > g and r > b:
            red_pixels += 1
        elif g > 100 and g > r and g > b + 30:
            green_pixels += 1
            print("here")
    if red_pixels > green_pixels:
        print(f"Taken username: {name}")
    elif green_pixels > red_pixels:
        print(f"Not Taken Username: {name}")
        with open("usernames.txt", "a") as f:
            f.write(f"{name}\n")


def all_valid_names():
    for combo in itt.product(CHARACTER_POOL, repeat=TARGET_USERNAME_LENGTH):
        s = "".join(combo)
        if ".." not in s:
            yield s


screen_size = pwc.getScreenSize()
if screen_size is None:
    raise RuntimeError("Screen size is none | Please fix shit")

for window in pwc.getAllWindows():
    # discord_pids[0] is always going to be the main root GUI window
    if window.getPID() != discord_pids[0]:
        continue
    screen_w, screen_h = screen_size
    win_w, win_h = window.size
    x = (screen_w - win_w) // 2
    y = (screen_h - win_h) // 2
    window.moveTo(x, y)
    window.resizeTo(750, 750)
    pag.click(793, 884)
    pag.moveTo(567, 736)
    pag.scroll(6)
    time.sleep(0.1)
    pag.click(552, 400)
    pag.click(1159, 686)
    names = list(all_valid_names())
    random.shuffle(names)
    for name in names:
        handle_name(name)
        time.sleep(1)
