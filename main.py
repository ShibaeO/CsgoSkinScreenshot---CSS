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

def crop_talon(mode, img, id):
    if mode == "back":
        img = Image.open(str(img))
        border = (160, 81, 160, 81)  # left, up, right, bottom
        cropped = ImageOps.crop(img, border)
        rotated = cropped.rotate(65)
        border = (278, 159, 433, 159)  # left, up, right, bottom
        im = ImageOps.crop(rotated, border)

        pixels = im.load()

        width, height = im.size
        for x in range(width):
            for y in range(height):
                r, g, b = pixels[x, y]
                if (r, g, b) == (0, 0, 0):
                    pixels[x, y] = (45, 52, 54)

        im.save(f"{id}_backside.png", "png")

    elif mode == "play":
        img = Image.open(str(img))
        border = (160, 81, 160, 81)  # left, up, right, bottom
        cropped = ImageOps.crop(img, border)
        test = cropped.rotate(-65)
        border = (408, 159, 274, 159)  # left, up, right, bottom
        im = ImageOps.crop(test, border)

        pixels = im.load()

        width, height = im.size
        for x in range(width):
            for y in range(height):
                r, g, b = pixels[x, y]
                if (r, g, b) == (0, 0, 0):
                    pixels[x, y] = (45, 52, 54)

        im.save(f"{id}_playside.png", "png")

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
    time.sleep(2.5)

    save_path = f"{id}_playside.png"
    ImageGrab.grab().save(save_path)
    time.sleep(1)

    pyautogui.moveTo(clickx, clicky)
    pyautogui.drag(-380, 0, 2, button='left')
    save_path = f"{id}_backside.png"
    time.sleep(1)
    ImageGrab.grab().save(save_path)

   # if weaponType == "Bayonet" or weaponType == "Karambit" or weaponType == "Shadow Daggers" or "Gloves" in weaponType or "Knife" in weaponType:
    #    save_path = f"{id}_playside.png"
   #     crop_knife("play", save_path, id)
    #    save_path = f"{id}_backside.png"
    #    crop_knife("back", save_path, id)
    if weaponType == "Karambit" or weaponType == "Talon Knife":
        save_path = f"{id}_backside.png" # iverser car le premier scree pris est le back side pour le talon
        crop_talon("play", save_path, id)
        save_path = f"{id}_playside.png"
        crop_talon("back", save_path, id)
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


def main(url, id):
    global super_Var_lol
    super_Var_lol = get_window_info("CS:GO MIGI")
    print("Got CSGO Window")
    print(f"[+] {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} -----> Taking screenshot of item id : {id}")
    while True:

        focus_window()
        screen(url, id)

        break

"""#pistol test
url = [
    "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20M567835434500285294A6890278457D7217761984680802747",
    "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20M633137629093035679A7009582189D7676003762701880389",
    "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20M1970780032104770464A14931685006D769557030645564088",
    "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20M567835434501727074A7013725658D7837503774794473695",
    "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20M629759929377113726A7013816152D315399352133020036",
    "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20M566709534597094873A7017038068D11963933693086198882",
    "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20M567835434504017014A7014852070D11576539041362223596",
    "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20M192910765526620051A7001529540D10278484185962303182",
    "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20M567838199905072112A7223698097D13881260557936212958",
    "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20M280752834392830333A9475872382D7791900731263490827",
        ]
"""

"""url = [
    "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20S76561198251702978A7004230400D903048837917845911",
    "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20S76561198254147490A6935333937D55310245988069934",
    "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20M628634029467888445A6995083397D6983640911094414019",
    "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20M573463979402187374A6847585353D9683911451363831966",
    "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20M1982033163480175927A14698000126D6939559547703154843",
    "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20M567835434498245724A7008651367D579312905880222669",
    "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20M1968528232297296432A14935104083D7812692350590599050",
    "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20M191784865621576470A7006284852D2460197461240251630",
    "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20M570089999715578734A7219360283D9578699314150025598",
    "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20M1969653972789156223A14926450430D3026986756764264255",
    "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20M567835434496842504A7006292395D7809422409315546280",
]
"""

url = [
    "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20M1975277764044161561A14702751549D7065844438316666997",
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

