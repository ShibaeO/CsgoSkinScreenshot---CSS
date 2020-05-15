import json
import os
import time
from datetime import datetime
from config import huey
import pyautogui
import requests
import win32gui
from PIL import ImageGrab, Image, ImageOps, ImageDraw, ImageFont
import redis
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
            # print("Window \"%s\":" % win32gui.GetWindowText(hwnd))
            # print("\tLocation: (%d, %d)" % (x, y))
            # print("\t    Size: (%d, %d)" % (w, h))
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
        border = (80, 230, 80, 180)  # left, up, right, bottom
        cropped = ImageOps.crop(im, border)
        cropped.save(f"{id}_playside.png", "png")
    elif mode == "back":
        im = Image.open(str(img))
        border = (80, 250, 80, 180)  # left, up, right, bottom
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

def crop_glove(mode, img, id):
    if mode == "play":
        im = Image.open(str(img))
        border = (440, 50, 440, 350)  # left, up, right, bottom
        cropped = ImageOps.crop(im, border)
        cropped.save(f"{id}_playside.png", "png")
    elif mode == "back":
        im = Image.open(str(img))
        border = (440, 50, 440, 350)  # left, up, right, bottom
        cropped = ImageOps.crop(im, border)
        cropped.save(f"{id}_backside.png", "png")

def crop_talon(mode, img, id):
    print(img)
    if mode == "back":
        img = Image.open(img)
        img = img.rotate(-90)
        border = (456, 340, 474, 140)  # left, up, right, bottom
        im = ImageOps.crop(img, border)
        im.save(f"{id}_backside.png", "png")

    elif mode == "play":
        img = Image.open(img)
        img = img.rotate(90)
        border = (456, 340, 474, 140)  # left, up, right, bottom
        im = ImageOps.crop(img, border)
        im.save(f"{id}_playside.png", "png")


def crop_sticker_final(img, id, data):
    img = Image.open(img)
    border = (400, 200, 400, 200)  # left, up, right, bottom
    im = ImageOps.crop(img, border)
    im.save(f"{id}_playside.png", "png")

    fullName = data["iteminfo"]["full_item_name"].replace("★", "")
    sep = Image.new('RGB', (1760, 60), color=(24, 128, 122))
    d = ImageDraw.Draw(sep)
    font = ImageFont.truetype("ressources/Bison.ttf", 25)
    d.multiline_text((20, 14), f"{fullName}        Shibaeo <3", fill=(255, 255, 0), spacing=4, align="left", font=font)
    sep.save('ressources/sep.png', "png")

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
    floatVal = data["iteminfo"]["floatvalue"]
    fullName = data["iteminfo"]["full_item_name"].replace("★", "")
    sep = Image.new('RGB', (1760, 60), color=(24, 128, 122))
    d = ImageDraw.Draw(sep)
    font = ImageFont.truetype("ressources/Bison.ttf", 25)
    d.multiline_text((20, 14), f"{fullName}        PaintID : {paintID}        float : {floatVal}        Shibaeo <3",
                     fill=(255, 255, 0), spacing=4, align="left", font=font)
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
        crop_talon("back", save_path, id)
        save_path = f"{id}_playside.png"
        crop_talon("play", save_path, id)
        time.sleep(1)
        final_image(id, data)

    elif weaponType == "Bayonet" or weaponType == "Karambit" or weaponType == "Shadow Daggers" or "Knife" in weaponType:
        save_path = f"{id}_playside.png"
        crop_knife("play", save_path, id)
        save_path = f"{id}_backside.png"
        crop_knife("back", save_path, id)
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
    print(f"         [+] {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} Got CSGO Window")
    print(f"         [+] {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} -----> Taking screenshot of item id : {id}")
    print(f"         [+] {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} Queue size : {r.get('queue')}\n")
    while True:

        focus_window()
        screen(url, id)

        r.decr("queue")
        r.incr("total_scr")
        break


#place url here :
"""url = [
    "steam://rungame/730/76561202255233023/+csgo_econ_action_preview S76561198106428990A15181179134D4911215139517499306",
    "steam://rungame/730/76561202255233023/+csgo_econ_action_preview S76561198213656201A7496627946D4911215139517499306",
]"""
#url_end


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