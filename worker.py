import json
import os
import time
from datetime import datetime

import pyautogui
import redis
import requests
import win32gui
from PIL import ImageGrab, Image, ImageOps, ImageDraw, ImageFont

from config import huey

r = redis.Redis(host='localhost', port=6379, db=0)


def get_window_info(window_name):
    window = {}

    def callback(hwnd, extra):
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y
        if win32gui.GetWindowText(hwnd) == window_name:
            location = {"x": x, "y": y}
            size = {"x": w, "y": h}
            window["location"] = location
            window["size"] = size

    win32gui.EnumWindows(callback, None)
    return window


def focus_window():
    startx = super_Var_lol["size"]["x"] / 2
    clickx = super_Var_lol["location"]["x"] + startx
    clicky = super_Var_lol["location"]["y"] + 5
    pyautogui.moveTo(clickx, clicky)
    time.sleep(0.1)
    pyautogui.click()


def crop(mode, img, id):
    if mode == "play":
        im = Image.open(str(img))
        border = (64, 230, 64, 180)  # left, up, right, bottom
        cropped = ImageOps.crop(im, border)
        cropped.save(f"{id}_cropped_playside.png", "png")
        os.remove(f"{id}_playside.png")
    elif mode == "back":
        im = Image.open(str(img))
        border = (64, 250, 64, 180)  # left, up, right, bottom
        cropped = ImageOps.crop(im, border)
        cropped.save(f"{id}_cropped_backside.png", "png")
        os.remove(f"{id}_backside.png")


def crop_knife(mode, img, id, ktype):
    if ktype == "all":
        if mode == "play":
            im = Image.open(str(img))
            border = (64, 30, 64, 250)  # left, up, right, bottom
            cropped = ImageOps.crop(im, border)
            cropped.save(f"{id}_cropped_playside.png", "png")
            os.remove(f"{id}_playside.png")
        elif mode == "back":
            im = Image.open(str(img))
            border = (64, 30, 64, 250)  # left, up, right, bottom
            cropped = ImageOps.crop(im, border)
            cropped.save(f"{id}_cropped_backside.png", "png")
            os.remove(f"{id}_backside.png")

    if ktype == "tiger":
        if mode == "play":
            im = Image.open(str(img))
            border = (3, 75, 125, 205)  # left, up, right, bottom
            cropped = ImageOps.crop(im, border)
            cropped.save(f"{id}_cropped_playside.png", "png")
            os.remove(f"{id}_backside.png")
        elif mode == "back":
            im = Image.open(str(img))
            border = (125, 75, 3, 205)  # left, up, right, bottom
            cropped = ImageOps.crop(im, border)
            cropped.save(f"{id}_cropped_backside.png", "png")
            os.remove(f"{id}_playside.png")


def crop_glove(mode, img, id):
    if mode == "play":
        im = Image.open(str(img))
        border = (128, 50, 128, 350)  # left, up, right, bottom
        cropped = ImageOps.crop(im, border)
        cropped.save(f"{id}_cropped_playside.png", "png")
        os.remove(f"{id}_playside.png")
    elif mode == "back":
        im = Image.open(str(img))
        border = (64, 50, 64, 350)  # left, up, right, bottom
        cropped = ImageOps.crop(im, border)
        cropped.save(f"{id}_cropped_backside.png", "png")
        os.remove(f"{id}_backside.png")


def crop_sticker_final(img, id, data):
    img = Image.open(img)
    border = (112, 200, 112, 200)  # left, up, right, bottom
    im = ImageOps.crop(img, border)
    im.save(f"{id}_playside.png", "png")

    fullName = data["iteminfo"]["full_item_name"].replace("★", "")

    sep = Image.open("ressources/sep_template.png")
    d = ImageDraw.Draw(sep)
    floatFont = ImageFont.truetype("ressources/Futura.ttf", 30)
    mainTextFont = ImageFont.truetype("ressources/FuturBold.ttf", 40)
    d.multiline_text((173, 11), f"None", fill=(225, 256, 41), font=floatFont)
    d.multiline_text((102, 52), f"None", fill=(225, 256, 41), font=floatFont)
    d.multiline_text((650, 25), f"{fullName}", fill=(225, 256, 41), font=mainTextFont)
    sep.save("ressources/sep.png")

    im1 = Image.open(f"{id}_playside.png")
    im3 = Image.open("ressources/sep.png")
    dst = Image.new('RGB', (im1.width, im1.height + im3.height))
    dst.paste(im1, (0, 0))
    dst.paste(im3, (0, im1.height))
    dst.save(f"scr/{id}.png", "png")
    os.remove(f"{id}_playside.png")
    os.remove(f"{id}_backside.png")
    os.remove(f"ressources/sep.png")


def final_image(id, data):
    paintID = data["iteminfo"]["paintseed"]
    floatVal = float(data["iteminfo"]["floatvalue"])
    fullName = data["iteminfo"]["full_item_name"].replace("★", "")

    if floatVal > 0.45:
        floatColor = (255, 0, 0)
    elif floatVal > 0.38 and floatVal < 0.45:
        floatColor = (255, 127, 80)
    elif floatVal > 0.15 and floatVal < 0.38:
        floatColor = (255, 165, 0)
    elif floatVal > 0.07 and floatVal < 0.15:
        floatColor = (64, 224, 208)
    elif floatVal > 0.0 and floatVal < 0.07:
        floatColor = (173, 255, 47)

    sep = Image.open("ressources/sep_template.png")
    d = ImageDraw.Draw(sep)
    floatFont = ImageFont.truetype("ressources/Futura.ttf", 30)
    mainTextFont = ImageFont.truetype("ressources/FuturBold.ttf", 40)
    d.multiline_text((173, 11), f"{paintID}", fill=(225, 256, 41), font=floatFont)
    d.multiline_text((102, 52), f"{floatVal}", fill=floatColor, font=floatFont)
    d.multiline_text((650, 25), f"{fullName}", fill=(225, 256, 41), font=mainTextFont)
    sep.save("ressources/sep.png")

    im1 = Image.open(f"{id}_cropped_playside.png")
    im2 = Image.open(f"{id}_cropped_backside.png")
    im3 = Image.open("ressources/sep.png")
    dst = Image.new('RGB', (im1.width, im1.height + im3.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im3, (0, im2.height))
    dst.paste(im2, (0, im2.height + im3.height))
    dst.save(f"scr/{id}.png", "png")
    os.remove(f"{id}_cropped_playside.png")
    os.remove(f"{id}_cropped_backside.png")
    os.remove(f"ressources/sep.png")


def screen(url, id):
    infoUrl = f"https://api.csgofloat.com/?url={url}"
    data = json.loads(requests.get(infoUrl).text)

    weaponType = data["iteminfo"]["weapon_type"]

    clickx = super_Var_lol["size"]["x"] * 0.80
    clicky = super_Var_lol["size"]["y"] * 0.80
    os.system(f'start {url}')
    time.sleep(2.5)

    save_path = f"{id}_playside.png"
    ImageGrab.grab().save(save_path)
    time.sleep(1)

    pyautogui.moveTo(clickx, clicky)
    pyautogui.drag(-380, 0, 2, button='left')
    save_path = f"{id}_backside.png"
    time.sleep(1)
    ImageGrab.grab().save(save_path)

    if weaponType == "Karambit" or weaponType == "Talon Knife":
        save_path = f"{id}_backside.png"
        crop_knife("play", save_path, id, ktype="tiger")
        save_path = f"{id}_playside.png"
        crop_knife("back", save_path, id, ktype="tiger")
        time.sleep(1)
        final_image(id, data)

    elif weaponType == "Bayonet" or weaponType == "Shadow Daggers" or "M9" in weaponType or "Knife" in weaponType:
        save_path = f"{id}_playside.png"
        crop_knife("play", save_path, id, ktype="all")
        save_path = f"{id}_backside.png"
        crop_knife("back", save_path, id, ktype="all")
        time.sleep(1)
        final_image(id, data)

    elif weaponType == "Sticker" or "Pin" in weaponType or "Graffiti" in weaponType:
        print("pin")
        save_path = f"{id}_playside.png"
        crop_sticker_final(save_path, id, data)

    elif "Gloves" in weaponType or "Wraps" in weaponType:
        save_path = f"{id}_playside.png"
        crop_glove("play", save_path, id)
        save_path = f"{id}_backside.png"
        crop_glove("back", save_path, id)
        time.sleep(1)
        final_image(id, data)

    else:
        save_path = f"{id}_playside.png"
        crop("play", save_path, id)
        save_path = f"{id}_backside.png"
        crop("back", save_path, id)
        time.sleep(1)
        final_image(id, data)


def url_parse(url):
    splitedUrl = url.split("/")
    parsedUrl = splitedUrl[5].replace("+csgo_econ_action_preview%20", "")
    return parsedUrl


@huey.task()
def main(url, id):
    global super_Var_lol

    super_Var_lol = get_window_info("CS:GO MIGI")
    print(f"         ")
    print(f"         [+] {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} Got CSGO Window")
    print(f"         [+] {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} -----> Taking screenshot of item id : {id}")
    print(f"         [+] {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} Queue size : {r.get('queue')}\n")
    while True:
        focus_window()
        screen(url, id)

        r.decr("queue")
        r.incr("total_scr")
        break


# place url here :
"""url = [
    "steam://rungame/730/76561202255233023/+csgo_econ_action_preview S76561198106428990A15181179134D4911215139517499306",
    "steam://rungame/730/76561202255233023/+csgo_econ_action_preview S76561198213656201A7496627946D4911215139517499306",
]"""
# url_end


"""if __name__ == '__main__':
    totalTime = 0
    for x in url:
        id = url_parse(x)
        start_time = time.time()
        main(x)
        end_time = time.time()
        totalTime += end_time - start_time
        print(f"screenshot taken in : {end_time - start_time} s\n   ")

    print(f"total screnshots time : {totalTime}")
"""
