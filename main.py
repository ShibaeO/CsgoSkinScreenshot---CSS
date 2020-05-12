import json
import win32gui
import pyautogui
import time
import os
import requests
import random
from datetime import datetime
from PIL import ImageGrab, Image, ImageOps, ImageDraw, ImageFont

def get_window_info(window_name):
    window = {}
    def callback(hwnd, extra):
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y
        if win32gui.GetWindowText(hwnd) == window_name:
            #print("Window \"%s\":" % win32gui.GetWindowText(hwnd))
            #print("\tLocation: (%d, %d)" % (x, y))
            #print("\t    Size: (%d, %d)" % (w, h))
            location = {"x": x, "y": y}
            size = {"x": w, "y": h}
            window["location"] = location
            window["size"] = size
    win32gui.EnumWindows(callback, None)
    return window

def focus_window():
    startx = super_Var_lol["size"]["x"]/2
    clickx = super_Var_lol["location"]["x"] + startx
    clicky = super_Var_lol["location"]["y"] + 5
    pyautogui.moveTo(clickx,clicky)
    time.sleep(0.1)
    pyautogui.click()

def crop(mode, img, id):
    if mode == "play":
        im = Image.open(str(img))
        border = (80, 200, 80, 200)  # left, up, right, bottom
        cropped = ImageOps.crop(im, border)
        cropped.save(f"{id}_playside.png", "png")
    elif mode == "back":
        im = Image.open(str(img))
        border = (80, 200, 80, 200)  # left, up, right, bottom
        cropped = ImageOps.crop(im, border)
        cropped.save(f"{id}_backside.png", "png")

def crop_knife(mode, img, id):
    if mode == "play":
        im = Image.open(str(img))
        border = (640, 81, 640, 81)  # left, up, right, bottom
        cropped = ImageOps.crop(im, border)
        cropped = cropped.transpose(Image.ROTATE_90)
        cropped.save(f"{id}_playside.png", "png")
    elif mode == "back":
        im = Image.open(str(img))
        border = (640, 81, 640, 81)  # left, up, right, bottom
        cropped = ImageOps.crop(im, border)
        cropped = cropped.transpose(Image.ROTATE_270)
        cropped.save(f"{id}_backside.png", "png")
#2d3436

def final_image(id, data):

    paintID = data["iteminfo"]["paintseed"]
    floatVal = data["iteminfo"]["floatvalue"]
    fullName = data["iteminfo"]["full_item_name"].replace("★", "")
    sep = Image.new('RGB', (1760, 60), color=(24, 128, 122))
    d = ImageDraw.Draw(sep)
    font = ImageFont.truetype("ressources/Bison.ttf", 25)
    d.multiline_text((20, 14), f"{fullName}        PaintID : {paintID}        float : {floatVal}        Shibaeo <3", fill=(255, 255, 0), spacing=4, align="left", font=font)
    sep.save('ressources/sep.png', "png")

    im1 = Image.open(f"{id}_playside.png")
    im2 = Image.open(f"{id}_backside.png")
    im3 = Image.open("ressources/sep.png")
    dst = Image.new('RGB', (im1.width, im1.height + im3.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im3, (0, im2.height))
    dst.paste(im2, (0, im2.height + im3.height))
    dst.save(f"scr/{id}.png", "png")
    os.remove(f"{id}_playside.png")
    os.remove(f"{id}_backside.png")
    os.remove(f"ressources/sep.png")


def screen(url, id):

    infoUrl = f"https://api.csgofloat.com/?url={url}"
    data = json.loads(requests.get(infoUrl).text)

    weaponType = data["iteminfo"]["weapon_type"]

    clickx = super_Var_lol["size"]["x"] * 0.80
    clicky = super_Var_lol["size"]["y"] * 0.80
    os.system(f'start {url}')
    time.sleep(1.5)

    save_path = f"{id}_playside.png"
    ImageGrab.grab().save(save_path)
    time.sleep(1)

    pyautogui.moveTo(clickx, clicky)
    pyautogui.drag(-380, 0, 2, button='left')
    save_path = f"{id}_backside.png"
    time.sleep(1)
    ImageGrab.grab().save(save_path)

    if "Knife" in weaponType or weaponType == "Bayonet" or weaponType == "Karambit" or weaponType == "Shadow Daggers":
        save_path = f"{id}_playside.png"
        crop_knife("play", save_path, id)
        save_path = f"{id}_backside.png"
        crop_knife("back", save_path, id)
    else:
        save_path = f"{id}_playside.png"
        crop("play", save_path, id)
        save_path = f"{id}_backside.png"
        crop("back", save_path, id)

    time.sleep(1)

    final_image(id, data)

    #-75 pour metre droit
    #-370 pour back side

def url_parse(url):
    splitedUrl = url.split("/")
    parsedUrl = splitedUrl[5].replace("+csgo_econ_action_preview%20", "")
    return parsedUrl


def main(url, id):
    global super_Var_lol
    super_Var_lol = get_window_info("CS:GO MIGI")
    print("Got CSGO Window")
    print(f"[+] {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} -----> Taking screenshot of item id : {id}")
    while True:

        focus_window()
        screen(url, id)

        break

url = [
    #"steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20M632011729189536458A7008814011D12295506487237922602",
    #"steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20S76561198251702978A7004230400D903048837917845911",
    #"steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20M633138486229823008A7022654840D614823716239812366",
    #"steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20S76561198255004025A6980175061D9262440886311016501",
    #"steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20M283004634227196325A9520265790D12538699143338037188",
    #"steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20M1911141422672709113A16990064703D9387373730855472081",
    #"steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20M3167648443666738410A17182190108D336820863276418395",
    "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20S76561198822504212A18491077225D9693978678799666676"
        ]


if __name__ == '__main__':
    totalTime = 0
    for x in url:
        id = url_parse(x)
        start_time = time.time()
        main(x, id)
        end_time = time.time()
        totalTime += end_time - start_time
        print(f"screenshot taken in : {end_time - start_time} s\n   ")

    print(f"total screnshots time : {totalTime}")

