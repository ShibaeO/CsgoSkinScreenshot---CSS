import win32gui
import pyautogui
import time
import os
import threading
from PIL import ImageGrab, Image, ImageOps

def get_window_info(window_name):
    window = {}
    def callback(hwnd, extra):
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y
        if win32gui.GetWindowText(hwnd) == window_name:
            print("Window \"%s\":" % win32gui.GetWindowText(hwnd))
            print("\tLocation: (%d, %d)" % (x, y))
            print("\t    Size: (%d, %d)" % (w, h))
            location = {"x": x, "y": y}
            size = {"x": w, "y": h}
            window["location"] = location
            window["size"] = size
    win32gui.EnumWindows(callback, None)
    return window

def focus_window():
    startx = test["size"]["x"]/2
    clickx = test["location"]["x"] + startx
    clicky = test["location"]["y"] + 5
    pyautogui.moveTo(clickx,clicky)
    time.sleep(0.1)
    pyautogui.click()

def crop(mode, img, id):
    if mode == "play":
        im = Image.open(str(img))
        border = (80, 225, 80, 268)  # left, up, right, bottom
        cropped = ImageOps.crop(im, border)
        cropped.save(f"{id}_playside.png", "png")
    elif mode == "back":
        im = Image.open(str(img))
        border = (80, 225, 80, 268)  # left, up, right, bottom
        cropped = ImageOps.crop(im, border)
        cropped.save(f"{id}_backside.png", "png")

def final_image(id):
    im1 = Image.open(f"{id}_playside.png")
    im2 = Image.open(f"{id}_backside.png")
    im3 = Image.open("sep.png")
    dst = Image.new('RGB', (im1.width, im1.height + im3.height + im2.height))
    dst.paste(im2, (0, 0))
    dst.paste(im3, (0, im2.height))
    dst.paste(im1, (0, im2.height + im3.height))
    dst.save(f"{id}_final.png", "png")
    os.remove(f"{id}_playside.png")
    os.remove(f"{id}_backside.png")


def screen():
    clickx = test["size"]["x"] * 0.80
    clicky = test["size"]["y"] * 0.80
    pyautogui.moveTo(clickx, clicky)
    pyautogui.drag(-75, 0, 2, button='left')
    id = 1
    save_path = f"{id}_playside.png"
    time.sleep(1.5)
    ImageGrab.grab().save(save_path)
    crop("play", save_path, id)

    pyautogui.moveTo(clickx, clicky)
    pyautogui.drag(-370, 0, 2, button='left')
    save_path = f"{id}_backside.png"
    time.sleep(1.5)
    ImageGrab.grab().save(save_path)
    crop("back", save_path, id)

    time.sleep(1)
    final_image(id)

    #-75 pour metre droit
    #-370 pour back side


def main():
    global test
    test = get_window_info("Counter-Strike: Global Offensive")
    print("Got CSGO Window")
    while True:
        focus_window()
        os.system('start steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20S76561198822504212A18491075281D922218567586923246')
        print("\nMoving to the skin")
        time.sleep(2)
        screen()
        break

if __name__ == '__main__':
    main()
