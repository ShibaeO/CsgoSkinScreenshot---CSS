from PIL import Image, ImageDraw,ImageFont, ImageOps, ImageGrab
import sys


"""im1 = Image.open("8_backside.png")
border = (640, 81, 640, 81)  # left, up, right, bottom
out = im1.transpose(Image.ROTATE_270)
out.save("test.png", "png")
bc = Image.new("RGB", (1760, 640), color=(45, 52, 54))
bc.save("bc.png", "png")


im1 = Image.open('test.png')
im2 = Image.open('bc.png')

blend = Image.blend(im1, im2, 0)
blend.save("final.pm", "png")
"""

"""
img = Image.open("1_playside.png")
#img1 = Image.open("final2.png")
#img2 = Image.open("final22.png")
#img3 = Image.open("sep.png")

border = (283, 382, 321, 291) # left, up, right, bottom
cropped = ImageOps.crop(img, border)
cropped.save("cropped_ar_play.png", "png")

def get_concat_v(im1, im2, im3):
    dst = Image.new('RGB', (im1.width, im1.height + im3.height + im2.height))
    dst.paste(im2, (0, 0))
    dst.paste(im3, (0, im2.height))
    dst.paste(im1, (0, im2.height + im3.height))

    return dst

#get_concat_v(img1, img2, img3).save("img3.png", "png")

# crop ar play side : border = (283, 382, 321, 291)
# crop ar back side : border = (321, 382, 283, 291)

"""
"""from steam.client import SteamClient
from csgo.client import CSGOClient
import logging

logging.basicConfig(format='[%(asctime)s] %(levelname)s %(name)s: %(message)s', level=logging.DEBUG)

client = SteamClient()
cs = CSGOClient(client)
@client.on('logged_on')
def start_csgo():
    print("logged")
    cs.launch()

@cs.on('ready')
def gc_ready():
    # send messages to gc
    print("ready")
    pass

client.cli_login(username="unshibasauvage", password="bobby810404")
client.run_forever()"""

"""
img = Image.new('RGB', (918, 60), color=(24, 128, 122))

float = "0.3839501440525055"
paintId = "932"
name = "★ Sport Gloves | Arid (Well-Worn)".replace("★", "")
font = ImageFont.truetype("ressources/Bison.ttf", 25)
d = ImageDraw.Draw(img)
d.multiline_text((50, 14), f"{name}        PaintID : {paintId}        float : {float}        Shibaeo <3", fill=(255, 255, 0), spacing=4, align="left", font=font)

img.save('pil_text.png')"""


ImageGrab.grab().save("ca.png")
img = Image.open("ca.png")
border = (400, 200, 400, 200)  # left, up, right, bottom
im = ImageOps.crop(img, border)
im.save("r2.png ", "png")
#border = (160, 81, 160, 81)  # left, up, right, bottom
#cropped = ImageOps.crop(img, border)
#ropped.save("cropped.png ", "png")

#draw = ImageDraw.Draw(cropped)
#draw.rectangle(((20, 10), (20, 10)), fill="white")
#draw.rectangle(((0, 0), (0, 0)), fill="white")



"""pixels = im.load()

width, height = im.size
for x in range(width):
    for y in range(height):
        r, g, b = pixels[x, y]
        if (r, g, b) == (0, 0, 0):
            pixels[x, y] = (45, 52, 54)
"""


"""img = Image.open("r.png")
img = img.convert("RGB")
pixdata = img.load()


for y in range(img.size[1]):
    for x in range(img.size[0]):
        if pixdata[x, y] == (0, 0, 0):
            pixdata[x, y] = (45, 52, 54)

"""
#pixdata.save("r.png ", "png")
#final.save("r.png ", "png")



"""-65 playside
65 back side"""

"""crop karambit : border = (341, 100, 341, 100)
crop talon :  border = (261, 100, 421, 100)"""